
// Vibration
int led = 12 ;
int buz = 7 ;
int vs = 9 ;

// Ultarsonic
const unsigned int TRIG_PIN=4;
const unsigned int ECHO_PIN=2;
const unsigned int LEDPIN2=3;
const unsigned int LEDPIN3=6;
const unsigned int LEDPIN=7; //ecco

void setup() {
  pinMode(vs, INPUT);
  pinMode(led, OUTPUT);
  pinMode(buz, OUTPUT); //vibration sensor

  pinMode(TRIG_PIN,OUTPUT);
  pinMode(ECHO_PIN,INPUT);
  pinMode(LEDPIN2,OUTPUT);
  pinMode(LEDPIN3,OUTPUT);//ecco
  Serial.begin(9600) ;
}
void loop() {
  
  long measurement = vibration() ;
  delay(50) ;
  
  if(measurement > 10000 && measurement < 20000) {
    digitalWrite(led, HIGH);  
    tone(buz,370) ;
    Serial.println("medium measurement") ;
  }

else if (measurement >= 20000) {
  digitalWrite(led,HIGH) ;
  tone(buz,740);
  Serial.println("high measurement") ;
  }
  else {
    digitalWrite(led, LOW);  
    noTone(buz) ;
  }

  //ecco
  long duration,dis;
  digitalWrite(TRIG_PIN,LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN,HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN,LOW);

  duration=pulseIn(ECHO_PIN,HIGH);
  dis =(duration/2)/29.1;

  //Serial.print(dis);
  //Serial.println(" cm");

  if(dis<14){
    digitalWrite(LEDPIN,HIGH);
    digitalWrite(LEDPIN2,HIGH);
    digitalWrite(LEDPIN3,LOW);
    //Serial.println("LED ON");
    Serial.println("close distance");
  }
  if(14<=dis && 16>=dis){
    digitalWrite(LEDPIN3,HIGH);
    Serial.println("medium distance") ;
  }
  else if(dis>16){ // so far makmak
    digitalWrite(LEDPIN,LOW);
    digitalWrite(LEDPIN2,LOW);
    digitalWrite(LEDPIN3,LOW);
    //Serial.println("LED Off");
    //Serial.println("dis>20") ;
    
  }
}
long vibration() {
  long measurement = pulseIn (vs,HIGH) ;
  return measurement ;
}
