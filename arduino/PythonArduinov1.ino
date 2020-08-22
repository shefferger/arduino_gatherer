String inChar;
#define LED 10
#define RedBTN 8
#define BlueBTN 9
#define WhiteBTN 6
#define Blue2BTN 7

bool isConnected = false;
bool btnState1 = false;
bool btnState2 = false; 
bool btnState3 = false; 
bool btnState4 = false; 

String pass = "E309229"; //секретное слово

void(* resetFunc) (void) = 0; // функция
                              // перезагрузки
void setup() {
  pinMode(LED, OUTPUT);
  for (int i = 6; i <= 9; i++)
    pinMode(i, INPUT);  //кнопки на вход
  Serial.begin(115200); //скорость соединения
}

void loop() {
  if (Serial.available() > 0) {   
    inChar = Serial.readString(); 
    if (!isConnected){            
      if (inChar == "search"){   
        Serial.print("imArduino");
      }
      if (inChar == pass){        
        isConnected = true;      
        Serial.print("ok");       
        analogWrite(LED, 140);
      }
    } 
    if (inChar == "reset"){
      analogWrite(LED, 0);
      Serial.print("Im resetting...");
      delay(50);
      resetFunc();
    }
  }  
  else{
    if (isConnected){ 
      if (digitalRead(BlueBTN) == HIGH && !btnState1){
        Serial.print("I");   //проверяем нажатие каждой клавиши
        btnState1 = true;    //и посылаем команду в порт
        delay(20);           //незабываем про задержку
      }                      //для защиты от дребезга
      if (digitalRead(BlueBTN) == LOW && btnState1){
        btnState1 = false;   //а также используем флаги
      }                      //чтобы засчитывалось только
                             //одно нажатие
      if (digitalRead(RedBTN) == HIGH && !btnState2){
        Serial.print("D");
        btnState2 = true;
        delay(10);                
      }
      if (digitalRead(RedBTN) == LOW && btnState2){
        btnState2 = false;
      }
      
      if (digitalRead(WhiteBTN) == HIGH && !btnState3){
        Serial.print("A");
        btnState3 = true;
        delay(10);                
      }
      if (digitalRead(WhiteBTN) == LOW && btnState3){
        btnState3 = false;
      }
      
      if (digitalRead(Blue2BTN) == HIGH && !btnState4){
        Serial.print("L");
        btnState4 = true;
        delay(10);                
      }
      if (digitalRead(Blue2BTN) == LOW && btnState4){
        btnState4 = false;
      }
      delay(3);
    }
  }
}

