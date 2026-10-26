from flask import Flask, render_template, request, Response, stream_with_context
import requests
import json

app = Flask(__name__)

# LLM Studio 로컬 서버 설정 (기본 포트: 1234 또는 사용 환경에 맞게 수정)
LLM_STUDIO_API_URL = "http://localhost:1235/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    purpose = data.get('purpose')
    duration = data.get('duration')
    destination_type = data.get('destination_type')
    companion = data.get('companion')
    companion_count = data.get('companion_count')

    # LLM에게 전달할 프롬프트 구성
    system_prompt = (
        "당신은 전문 여행 플래너입니다. 사용자의 여행 목적, 기간, 국내/국외 여부, 동반자 유형에 맞추어 "
        "최적의 맞춤형 여행 코스와 상세 일정을 작성해 주세요. "
        "일정은 날차별/구간별로 나누어 구체적이고 실용적으로 제안해 주세요."
    )
    
    user_prompt = (
        f"다음 조건에 맞는 상세한 여행 계획을 세워주세요:\n"
        f"- 여행 목적: {purpose}\n"
        f"- 여행 기간: {duration}\n"
        f"- 여행 지역: {destination_type}\n"
        f"- 동반자 유형: {companion} (총 {companion_count}명)\n\n"
        f"출력 형식은 마크다운을 사용하여 깔끔하게 정리해 주세요."
    )

    payload = {
        "model": "local-model", # LLM Studio에 로드된 모델 이름 (상황에 맞게 변경 가능)
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "stream": True # 실시간 스트리밍 활성화
    }

    def generate():
        try:
            # 1단계: 분석 단계 알림 (사용자 피드백용)
            yield f"data: {json.dumps({'status': 'analyzing', 'message': '🔍 사용자의 여행 조건(목적, 동반자, 기간)을 분석하고 최적의 코스를 구상 중입니다...'})}\n\n"
            
            response = requests.post(LLM_STUDIO_API_URL, json=payload, stream=True, timeout=60)
            
            if response.status_code != 200:
                yield f"data: {json.dumps({'status': 'error', 'message': '❌ LLM Studio 서버 연결에 실패했습니다. 서버가 켜져 있는지 확인해주세요.'})}\n\n"
                return

            # 2단계: 생성 시작 알림
            yield f"data: {json.dumps({'status': 'generating', 'message': '✍️ 맞춤형 여행 일정을 작성하고 있습니다...\n\n'})}\n\n"

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        json_str = decoded_line[6:]
                        if json_str.strip() == "[DONE]":
                            break
                        try:
                            chunk_data = json.loads(json_str)
                            delta = chunk_data.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                # 생성 중인 텍스트 조각 전송
                                payload_data = {'status': 'chunk', 'content': content}
                                yield f"data: {json.dumps(payload_data)}\n\n"
                        except json.JSONDecodeError:
                            continue
                            
            # 완료 알림
            yield f"data: {json.dumps({'status': 'done', 'message': ''})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': f'❌ 오류 발생: {str(e)}'})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)