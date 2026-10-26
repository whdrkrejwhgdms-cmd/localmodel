import random

# 문제와 답안 딕셔너리 생성
quiz = {
    "1 + 1": "2",
    "2 + 3": "5",
    "3 + 7": "10",
    "4 + 2": "6",
    "5 + 9": "14"
}

# 문제 리스트 생성
questions = list(quiz.keys())

# 문제 순서를 무작위로 섞음
random.shuffle(questions)

# 맞춘 문제 개수와 틀린 문제 개수 초기화
correct_answers = 0
wrong_answers = 0

# 퀴즈 시작
for idx, question in enumerate(questions):
    print(f"[문제 {idx + 1}]")
    print(question)

    # 사용자 입력 받기
    answer = input("정답을 입력하세요: ")

    # 정답 확인
    if answer == quiz[question]:
        print("정답입니다!\n")
        correct_answers += 1
    else:
        print("오답입니다.\n")
        wrong_answers += 1

# 결과 출력
total_questions = len(questions)
print("퀴즈가 종료되었습니다.")
print(f"맞춘 문제 개수: {correct_answers}/{total_questions}")
print(f"틀린 문제 개수: {wrong_answers}/{total_questions}")

# 백분율 계산 및 출력
percentage = (correct_answers / total_questions) * 100
print(f"정답 비율: {percentage:.2f}%")