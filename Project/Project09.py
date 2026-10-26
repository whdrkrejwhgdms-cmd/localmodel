import time

print("클릭을 위해 엔터를 눌러주세요. 중단하려면 컨트롤+C를 눌러주세요.")
input()
print('시작')

# 시작 시간 기록
startTime = time.time()
lastTime = startTime
lapNumber = 1

try:
    while True:
        input()
        # 현재 lap의 경과 시간 계산
        lapTime = round(time.time() - lastTime, 2)
        # 전체 경과 시간 계산
        totaltime = round(time.time() - startTime, 2)
        # lap 정보 출력
        print('Lap %s: %s (%s)' % (lapNumber, totaltime, lapTime), end='')

        # lap 번호 증가
        lapNumber += 1
        lastTime = time.time()

except KeyboardInterrupt:
    print('\n\n종료')