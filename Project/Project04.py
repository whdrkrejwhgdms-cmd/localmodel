import subprocess

# 무선 네트워크 프로필 정보를 얻는다
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp949').split('\n')

# 프로필 이름만 추출한다
profiles = [i.split(":")[1][1:-1] for i in data if "모든 사용자 프로필" in i]

# 각 프로필의 Wi-Fi 키 정보를 얻는다
for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i,
                                       'key=clear']).decode('cp949').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "키 콘텐츠" in b]

    # 예외 처리를 통해 결과를 출력한다
    try:
        print("{:<30}| {:<}".format(i, results[0]))
    except IndexError:
        print("{:<30}| {:<}".format(i, ""))