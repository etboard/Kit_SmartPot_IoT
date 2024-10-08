# 스마트 화분 IoT 키트


## 스마트 화분 IoT 키트 설명

1. 똑똑한 화분이에요: 이 화분은 마법처럼 식물이 물이 필요한지 알 수 있어요.
2. 자동으로 물을 줘요: 식물에게 물이 필요하다고 판단되면, 스스로 물을 줄 수 있어요.
3. 화면이 있어요: 작은 화면이 있어서 식물의 상태를 볼 수 있어요.
4. 멀리서도 볼 수 있어요: 인터넷을 통해 멀리 있어도 휴대폰으로 화분의 상태를 확인할 수 있어요.
5. 우리가 조종할 수도 있어요: 휴대폰으로 명령을 내려 원할 때 물을 줄 수 있어요.

## 코드 설명

1. 마법의 도구 준비하기: 코드 맨 위쪽에서 사용할 도구들을 준비해요.
2. 화분의 눈과 손 만들기: 토양 수분 측정 핀(눈)과 펌프 핀(손)을 설정해요.
3. 화분의 두뇌 만들기: `et_setup()` 함수로 화분의 '두뇌'를 준비해요.
4. 화분의 일과 만들기: `et_loop()` 함수로 화분의 반복적인 일을 정해요.
5. 화분의 표정 만들기: `display_information()` 함수로 화면에 상태를 보여줘요.
6. 화분이 말하기: `send_message()` 함수로 화분의 상태를 알려줘요.
7. 화분이 듣기: `recv_message()` 함수로 우리의 명령을 받아들여요.

## 코드 분석

이 코드는 'Kit_SmartPot_IoT.py'라는 이름의 스마트 화분 IoT 시스템을 위한 MicroPython 프로그램입니다.  
ETboard라는 하드웨어 플랫폼을 사용하고 있습니다.

주요 기능:
- 토양 수분 측정
- 워터 펌프 제어
- OLED 디스플레이를 통한 정보 표시
- IoT 기능을 통한 원격 모니터링 및 제어

주요 컴포넌트:
- 토양 수분 센서 (A3 핀)
- 워터 펌프 (D2, D3 핀)
- 작동 모드 LED (D4 핀)
- OLED 디스플레이

작동 모드:
- 자동 모드: 토양 수분 레벨에 따라 자동으로 워터 펌프 제어
- 수동 모드: 원격으로 워터 펌프 제어 가능

## 활용 방안

1. 식물 성장 관찰 일기: 매일 화분의 상태를 확인하고 기록해보세요.
2. 식물 돌보기 대회: 친구들과 함께 식물 키우기 대회를 해보세요.
3. 과학 실험하기: 다양한 조건을 변경해가며 식물 성장을 관찰해보세요.
4. 프로그래밍 배우기: 코드의 간단한 부분을 변경해보며 프로그래밍을 배워보세요.
5. IoT 체험하기: 스마트폰으로 화분을 원격 제어해보세요.
6. 창의적인 화분 꾸미기: 화분을 자신만의 스타일로 꾸며보세요.
7. 식물 이야기 만들기: 식물에게 이름을 지어주고 이야기를 만들어보세요.
8. 환경 보호 프로젝트: 식물의 중요성과 환경 보호에 대해 배워보세요.

이 스마트 화분 IoT 키트를 통해 초등학생들은 과학, 기술, 환경, 창의성 등 다양한 영역에서 학습하고 성장할 수 있습니다.
