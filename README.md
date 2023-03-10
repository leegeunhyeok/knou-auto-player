<div align="center">

  # knou-auto-player

  방송통신대학교 U-KNOU 캠퍼스 강의 자동 재생 플레이어

  ![image](https://user-images.githubusercontent.com/26512984/224306078-e4512805-7945-403e-a35d-8437402a8416.png)

</div>

## 주요 기능

[![asciicast](https://asciinema.org/a/ugbypzZQMiZiSQKJWJRfIiGA2.svg)](https://asciinema.org/a/ugbypzZQMiZiSQKJWJRfIiGA2)

- 자동 로그인
- 수강 중인 강좌 조회 및 자동 재생
  - 학습 완료 여부 감지
  - 준비 중인 영상 감지

> 업무 및 여러가지 스케줄로 인해 매번 강좌를 챙겨보기 어려워 개발하게 된 자동화 플레이어 입니다.
>
> 자동 재생에 지나치게 의존하여 학습 습관을 망치지 않도록 주의해주세요.

## 사전 요구사항

- Python 3.9
- Chrome 브라우저

## 환경 구성

```bash
# 의존성 설치
pip install -r requirements.txt
```

`config.ini` 파일 열어 계정 정보, 옵션을 지정한 후 저장합니다.

```
[player]
headless=1
mute_audio=1

[account]
id=
password=
```

- player.headless
  - 1: headless 모드 활성화 (브라우저 띄우지 않고 동작)
  - 0: 브라우저 띄운 상태로 동작
- player.mute_audio
  - 1: 모든 소리 음소거
  - 0: 모든 소리 재생

## 실행

```bash
python main.py
```

## 라이센스

[MIT](./LICENSE)
