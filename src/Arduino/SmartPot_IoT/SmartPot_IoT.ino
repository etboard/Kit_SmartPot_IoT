/******************************************************************************************
 * FileName     : SmartPot_IoT.ino
 * Description  : 이티보드 스마트 화분 코딩 키트(IoT)
 * Author       : SCS
 * Created Date : 2022.08.18
 * Reference    : 
 * Modified     : 2022.08.19 : LSC
 * Modified     : 2022.11.15 : YSY : D5 -> D2, 수분 단위 %
 * Modified     : 2022.12.27 : YSY : 변수 명명법 통일, 작동 모드 LED -> D4
 * Modified     : 2024.08.20 : SCS : 수분 센서 포트 정정(A0 -> A3)
 * Modified     : 2024.08.21 : SCS : 메시지 수신 & version 0.93 -> 0.94
 * Modified     : 2024.08.23 : SCS : 프로그램 구조 변경
 * Modified     : 2024.08.23 : SCS : setup_recv_message
 * Modified     : 2024.09.03 : PEJ : 펌프 상태 송신 로직 추가, clean
******************************************************************************************/
const char* board_firmware_verion = "smartPot_0.95";


//==========================================================================================
// IoT 프로그램 사용하기
//==========================================================================================
#include "ET_IoT_App.h"
ET_IoT_App app;


//==========================================================================================
// 전역 변수 선언
//==========================================================================================
int moisture_pin = A3;                                   // 토양수분 센서 핀: A3

int pump_pin1 = D2;                                      // 워터 펌프: Motor-L Pin1
int pump_pin2 = D3;                                      // 워터 펌프: Motor-L Pin2

int pump_state = 0;                                      // 워터 펌프 상태: 멈춤

int operation_mode_led = D4;                             // 작동 모드 LED: 녹색

const int moist_threshold = 30;                          // 30 %
int moisture_value;                                      // 토양 수분 값


//==========================================================================================
void et_setup()                                          // 사용자 맞춤형 설정
//==========================================================================================
{
  pinMode(pump_pin1, OUTPUT);                            // 모터 제어핀1: 출력 모드
  pinMode(pump_pin2, OUTPUT);                            // 모터 제어핀2; 출력 모드

  app.operation_mode = "automatic";                      // 작동 모드: 자동
  app.send_data("pump", "state", pump_state);            // 펌프 작동 상태 응답
  app.send_data("operation_mode", "mode", app.operation_mode);   // 작동 모드
}


//==========================================================================================
void et_loop()                                           // 사용자 반복 처리
//==========================================================================================
{
  do_sensing_process();                                  // 센싱 처리

  do_automatic_process();                                // 자동화 처리
}


//==========================================================================================
void do_sensing_process()                                // 센싱 처리
//==========================================================================================
{
  // 토양 수분 값 측정하여 100분율(%)로 환산
  moisture_value = map(analogRead(moisture_pin), 0, 2800, 100, 0);
}


//==========================================================================================
void do_automatic_process()                              // 자동화 처리
//==========================================================================================
{
  if(app.operation_mode != "automatic")                  // 작동 모드가 automatic 일 경우만
    return;

  // 토양수분이 값에 따라 워터 펌프의 작동 제어하기
  if (moisture_value < moist_threshold) {                // 토양수분 센서값이 moist_threshold 미만이면
    digitalWrite(pump_pin1, HIGH);                       // 워터 펌프: 작동
    digitalWrite(pump_pin2, LOW);                     
    app.dg_Write(pump_pin1, HIGH);   
    app.dg_Write(pump_pin2, LOW);   
    pump_state = 1;                                      // 워터 펌프 상태: 작동
  } else {
    digitalWrite(pump_pin1, LOW);                        // 워터 펌프: 멈춤
    digitalWrite(pump_pin2, LOW);                     
    app.dg_Write(pump_pin1, LOW);   
    app.dg_Write(pump_pin2, LOW);   
    pump_state = 0;                                      // 워터 펌프 상태: 멈춤
  }
}


//==========================================================================================
void et_short_periodic_process()                         // 사용자 주기적 처리 (예 : 1초마다)
//==========================================================================================
{
  display_information();                                 // 표시 처리
}


//==========================================================================================
void et_long_periodic_process()                          // 사용자 주기적 처리 (예 : 5초마다)
//==========================================================================================
{
  send_message();                                        // 메시지 송신
}


//==========================================================================================
void display_information()                               // OLED 표시
//==========================================================================================
{
  String string_moist = String(moisture_value);          // 수분 값을 문자열로 변환
  String string_pump = pump_state ? "On" : "Off";        // 1= On, 0=Off

  app.oled.setLine(1, board_firmware_verion);            // 1번째 줄에 펌웨어 버전
  app.oled.setLine(2, "moist: " + string_moist);         // 2번재 줄에 수분
  app.oled.setLine(3, "pump : " + string_pump);          // 3번재 줄에 펌프 작동 상태
  app.oled.display();                                    // OLED에 표시
}


//==========================================================================================
void send_message()                                      // 메시지 송신
//==========================================================================================
{
  app.add_sensor_data("moisture", moisture_value);       // 센서 데이터 추가
  app.send_sensor_data();                                // 센서 데이터 송신

  app.send_data("pump", "state", pump_state);            // 펌프 작동 상태 응답
  //app.send_data("operation_mode", "mode", app.operation_mode);   // 작동 모드
}


//==========================================================================================
void recv_message()                                      // 메시지 수신
//==========================================================================================
{
  // "operation_mode" 메시지를 받으면 process_operation_mode() 실행
  app.setup_recv_message("operation_mode", process_operation_mode);

  // "pump" 메시지를 받으면 process_pump_control() 실행
  app.setup_recv_message("pump", process_pump_control);
}


//==========================================================================================
void process_operation_mode(const String &msg)           // 작동 모드 처리
//==========================================================================================
{
  pinMode(operation_mode_led, OUTPUT);                   // 작동 모드 LED: 출력 모드 

  if (msg == "automatic") {                              // 작동 모드: 자동으로
    app.operation_mode = "automatic";
    digitalWrite(operation_mode_led, HIGH);
    Serial.println("작동모드: automatic, 녹색 LED on");
  } else {                                               // 자동 모드: 수동으로
    app.operation_mode = "manual";
    digitalWrite(operation_mode_led, LOW);
    Serial.println("작동모드: manual, 녹색 LED off");
  }
}


//==========================================================================================
void process_pump_control(const String &msg)             // 워터 펌프 제어 처리
//==========================================================================================
{
    // 자동 모드인 경우에는 워터 펌프를 원격에서 제어를 할 수 없음
    if (app.operation_mode == "automatic")
      return;

    // 수동 모드인 경우이면서
    if (msg == "1") {                                    // 1이면
      digitalWrite(pump_pin1, HIGH);                     // 워터 펌프: 작동
      digitalWrite(pump_pin2, LOW);
      pump_state = 1;
      Serial.println("워터 펌프: 작동");
    } else {                                             // 그렇지 않으면
      digitalWrite(pump_pin1, LOW);                      // 워터 펌프: 멈춤
      digitalWrite(pump_pin2, LOW);
      pump_state = 0;
      Serial.println("워터 펌프: 멈춤");
    }
    app.send_data("pump", "state", pump_state);          // 펌프 작동 상태 응답
}


//==========================================================================================
//                                                    
// (주)한국공학기술연구원 http://et.ketri.re.kr       
//                                                    
//==========================================================================================
