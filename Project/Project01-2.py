import random

# 정답과 오답 개수 초기화
correct_answers = 0
wrong_answers = 0

# 퀴즈 시작
print("퀴즈를 시작합니다.")

for idx in range(5):  # 5개의 문제를 무작위로 생성합니다.
    # 무작위로 숫자 생성
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(["+", "-", "*", "/"])

    # 문제와 정답 계산
    if operator == "+":
        question = f"{num1} + {num2}"
        answer = num1 + num2
    elif operator == "-":
        question = f"{num1} - {num2}"
        answer = num1 - num2
    elif operator == "*":
        question = f"{num1} * {num2}"
        answer = num1 * num2
    else:
        question = f"{num1} / {num2}"
        answer = num1 / num2

    print(f"[문제 {idx + 1}]")
    print(question)

    # 사용자 입력 받기
    user_answer = float(input("정답을 입력하세요: "))

    # 정답 확인
    if user_answer == answer:
        print("정답입니다!\n")
        correct_answers += 1
    else:
        print(f"오답입니다. 정답은 {answer}입니다.\n")
        wrong_answers += 1

# 결과 출력
total_questions = 5
print("퀴즈가 종료되었습니다.")
print(f"푼 문제 수: {correct_answers}/{total_questions}")
print(f"틀린 문제 수: {wrong_answers}/{total_questions}")

# 정확도 계산 및 출력
percentage = (correct_answers / total_questions) * 100
print(f"정확도: {percentage:.2f}%")