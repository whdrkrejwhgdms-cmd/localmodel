import random

# 비밀 숫자 생성
secret_number = random.randint(1, 20)

# 최대 시도 횟수 설정
max_attempts = 6

# 주어진 시도 횟수 동안 반복
for attempt in range(1, max_attempts + 1):
    print('-' * 100)
    print(f'남은 시도 횟수: {max_attempts - attempt + 1}')

    # 사용자로부터 숫자 입력 받기
    guess = int(input('추측 숫자를 입력하세요: '))

    # 사용자 입력과 비밀 숫자 비교하여 힌트 제공
    if guess < secret_number:
        print('예측 숫자가 너무 낮습니다.')
    elif guess > secret_number:
        print('예측 숫자가 너무 높습니다.')
    else:
        # 정답을 맞추면 루프 종료
        break

# 게임 결과 출력
if guess == secret_number:
    print(f'잘하셨습니다! {attempt}회 만에 맞추셨습니다.')
else:
    print(f'틀리셨습니다. 정답은 {secret_number}입니다.')
