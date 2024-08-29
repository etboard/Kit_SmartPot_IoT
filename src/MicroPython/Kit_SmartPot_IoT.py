# ******************************************************************************************
# FileName     : Kit_SmartPot_IoT.py
# Description  : 
# Author       : 손철수
# Created Date : 2024.08.20 : SCS 
# Reference    :
# Modified     : 2024.08.23 : SCS : clean
# ******************************************************************************************
board_firmware_verion = "smartPot_0.94";


#===========================================================================================
# 기본 모듈 사용하
#===========================================================================================
from machine import Pin
from ETboard.lib.pin_define import *                     # ETboard 핀 관련 모듈


#===========================================================================================
# IoT 프로그램 사용하기                       
#===========================================================================================
from ET_IoT_App import ET_IoT_App, setup, loop
app = ET_IoT_App()


#===========================================================================================
# OLED 표시 장치 사용하기
#===========================================================================================
from ETboard.lib.OLED_U8G2 import *
oled = oled_u8g2()


#===========================================================================================
# 아두이노 MAX 함수 구현
#===========================================================================================
def map(x,input_min,input_max,output_min,output_max):    # map 함수 정의
    return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min


#===========================================================================================
# 전역 변수 선언
#===========================================================================================
moisture_pin = ADC(Pin(A3))                              # 토양 수분 측정 핀: A3

pump_pin1 = Pin(D2)                                      # 워터 펌프 작동 핀 (Motor-L)
pump_pin2 = Pin(D3)                                      # 모터 작동 핀 (Motor-L)

pump_state = 0                                           # 워터 펌프 상태: 멈춤

operation_mode_led = Pin(D4)                             # 작동 모드 LED: 녹색

moist_threshold = 30                                     # 토양 수분 임계치: 30%
moisture_value =0                                        # 토양 수분 값



#===========================================================================================
def et_setup():                                          #  사용자 맞춤형 설정
#===========================================================================================
    moisture_pin.atten(ADC.ATTN_11DB)                    # 토양 수분 측정 센서 입력 모드 설정
    
    pump_pin1.init(Pin.OUT)                              # 모터 제어핀1: 출력 모드
    pump_pin2.init(Pin.OUT)                              # 모터 제어핀2: 출력 모드
    
    app.operation_mode = "automatic";                    # 작동 모드: 자동    
    app.send_data("pump", "state", pump_state);          # 펌프 작동 상태 응답
    app.send_data("operation_mode", "mode", app.operation_mode);   # 작동 모드    
    
    recv_message()                                       # 메시지 수신
    
    

#===========================================================================================
def et_loop():                                           # 사용자 반복 처리
#===========================================================================================
    do_sensing_proces()                                  # 센싱 처리
    do_automatic_process()                               # 자동화 처리


#===========================================================================================
def do_sensing_proces():                                 # 센싱 처리                     
#===========================================================================================    
    # 토양 수분 값 측정하여 100분율(%)로 환산   
    global moisture_value
    moisture_result = moisture_pin.read()                    # 토양 수분 측정값 저장
    moisture_value = map(moisture_result, 0, 2800, 100, 0)   # 토양 수분 측정값 % 변환 
   
    

#===========================================================================================
def do_automatic_process():                              # 자동화 처
#===========================================================================================
    if (app.operation_mode != 'automatic'):              # 작동 모드가 automatic 일 경우만
        return
    
    # 토양수분이 값에 따라 워터 펌프의 작동 제어하기
    global moisture_value, moist_threshold, pump_state
    if(moisture_value < moist_threshold) :               # 토양 수분 센서값이 moist_threshold 미만이면
        pump_pin1.value(HIGH)                            # 워터 펌프: 작동
        pump_pin2.value(LOW)
        pump_state = 1                                   # 워터 펌프 상태: 작동
    else :
        pump_pin1.value(LOW)                             # 워터 펌프: 멈춤
        pump_pin2.value(LOW)
        pump_state = 0                                   # 워터 펌프 상태: 멈춤
    
               
#===========================================================================================
def et_short_periodic_process():                         # 사용자 주기적 처리 (예 : 1초마다)
#===========================================================================================    
    display_information()                                # 표시 처리
    

#===========================================================================================
def et_long_periodic_process():                          # 사용자 주기적 처리 (예 : 5초마다)
#===========================================================================================    
    send_message()                                       # 메시지 송


#===========================================================================================
def display_information():                               # OLED 표시
#===========================================================================================
    global board_firmware_verion, moisture_value, pump_state                    
    string_mois = "%3d" % moisture_value                 # 수분 값을 문자열로 변환
    string_pump = 'On' if pump_state else 'Off'          # 1= On, 0=Off 
    
    oled.clear()                                         # OLED 초기화
    oled.setLine(1, board_firmware_verion)                      # 1번째 줄에 펌웨어 버전
    oled.setLine(2, 'moist: ' + string_mois)             # 2번째 줄에 수분
    oled.setLine(3, 'pump: '  + string_pump)             # 3번쩨 줄에 펌프 작동 상태    
    oled.display()                                       # OLED에 표시
    

#===========================================================================================
def send_message():                                      # 메시지 송신
#===========================================================================================
    global moisture_value
    app.add_sensor_data("moisture", moisture_value);     # 센서 데이터 추가
    app.send_sensor_data();                              # 센서 데이터 송신


#===========================================================================================
def recv_message():                                      # 메시지 송신
#===========================================================================================
    # "operation_mode" 메시지를 받으면 process_operation_mode() 실행
    app.setup_recv_message('operation_mode', process_operation_mode)
    
    # "pump" 메시지를 받으면 process_pump_control() 실행
    app.setup_recv_message('pump', process_pump_control)


#===========================================================================================
def process_operation_mode(topic, msg):                  # 작동 모드 처리
#===========================================================================================
    operation_mode_led.init(Pin.OUT)                     # 작동 모드 LED: 출력 모드
    
    if msg == "automatic":                               # 작동 모드: 자동으로
        app.operation_mode = "automatic"
        operation_mode_led.value(1)                      # LED 켜기
        print("작동모드: automatic, 녹색 LED on")
    else:                                                # 작동 모드: 수동으로
        app.operation_mode = "manual"
        operation_mode_led.value(0)                      # LED 끄기
        print("작동모드: manual, 녹색 LED off")


#===========================================================================================
def process_pump_control(topic, msg):                    # 워터 펌프 제어 처리
#===========================================================================================
    # 자동 모드인 경우에는 워터 펌프를 원격에서 제어를 할 수 없음
    if (app.operation_mode == 'automatic'): 
        return
    
    global pump_state
    if(msg == '1') :                                     # 토양 수분 센서값이 moist_threshold 미만이면
        pump_pin1.value(HIGH)                            # 워터 펌프 작동
        pump_pin2.value(LOW)
        pump_state = 1                                   # 워터 펌프 상태 On
        print('워터 펌프: 작동')
    else :
        pump_pin1.value(LOW)                             # 워터 펌프 작동 멈춤
        pump_pin2.value(LOW)
        pump_state = 0                                   # 워터 펌프 상태 Off
        print('워터 펌프: 멈춤')
        
    app.send_data("pump", "state", pump_state);          # 펌프 작동 상태 응답     

#===========================================================================================
# 시작 지점                     
#===========================================================================================
if __name__ == "__main__":
    setup(app, et_setup)
    while True:
        loop(app, et_loop, et_short_periodic_process, et_long_periodic_process)


#===========================================================================================
#                                                    
# (주)한국공학기술연구원 http://et.ketri.re.kr       
#
#===========================================================================================
