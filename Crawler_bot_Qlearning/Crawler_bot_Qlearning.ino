/*
A Q learning approach for a crawler robot
builidng on code base from jim demello
*/

// Servo setup:  the servos must be oriented so that if the arm is rotating counter-clockwise to the left of the servo, then up is 0 degrees
//               and down is 180 degrees, for both servos. Then when the arm is in it's highest postion, servo 1 (the servo closest to the
//               body of the robot, will be at 0 degrees and servo 2 will be at 40 degrees.)
// Sonar:        the ultrasonic module should be placed facing the rear of the robot as it measures movement of the robot away from some
//               solid structure like a wall.
// TODO:         1. smooth servo arm movements (simultaneous moves) - done
//               2. lower servo starting positions
//               3. try for 3 positions in success table
//               4. try using wheel encoder rather than ultrasonic module for greater precision and so that robot does not have to
//               measure distance from another object.
// algorithm:    this is a positive reinforcement (perhaps a simple greedy epsilon algorithm) unsupervised learning algorithm
//               It chooses a random state (arm position) for the first position then the second time in the loop randomly gets the second arm position
//               and then moves the arm from the first to the second position, gets distance moved and then if it is greater than
//               2cms, it stores these two arm movements in the successes table array.
//               When it has looped through the episodes number of cycles, it loops through the successes table to find the highest distance moved.
//               Then it just cycles back and forth through those two arm movements.
// improvements to algorithm: sometimes using just two arm positions is too little to produce much movement (although sometimes it is reallly good)
//                            so could change successes table to store 3 arm movements and then I think it would produce greater movement each time.
//
  
#include <VarSpeedServo.h> // use this lib rather than servo.h to control speed of servo
VarSpeedServo servo1,servo2;

float distance;
float sonarTime;

int TRIGGER=7,ECHO=8; // sonar pins
   
int pos[16][2]={  { 0,40}, // colum 1 holds servo1 positions and column 2 holds servo 2 positions
                  { 0,85},             
                  { 0,130},             
                  { 0,175},              
                  { 30,40},         
                  { 30,85},            
                  { 30,130},           
                  { 30,175},             
                  { 60,40},  
                  { 60,85},       
                  { 60,130},            
                  { 60,175},           
                  { 90,40},             
                  { 90,85},          
                  { 90,130},           
                  { 90,175}};      
int success[16] [5] = { // can have up to 16 successful moves. (from first arm postion) col1 is servo1, col2 is servo2 TO (second arm pos) col3 is servo2 and col4 is servo 2
                        // col 5 holds distance robot traveled after moving from arm position 1 to arm position 2
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0},
           {0,0,0,0,0}};
           

int state=0;
int numberSuccesses = 0;

int episodes = 0;
  int spos1 = 0;
  int spos2 = 0;
  int spos3 = 0;
  int spos4 =0;
  
  float distDifference=0,distPrevious=0,distCurrent=0;
   
void setup (){ 
  servo1.attach( 9, 600, 2400 );
  servo2.attach( 6, 600, 2400 );
  servo1.write(0,50); //starting position for servo 1
  servo2.write(0,50);
  delay(1000);
  
  pinMode(TRIGGER, OUTPUT); // setup sonar
  pinMode(ECHO, INPUT);
  Serial.begin(9600);

  randomSeed(analogRead(0));
 
  distPrevious = getDistance(); //get initial distance
  Serial.println(distPrevious);
  delay(1000);
 // exit(0);  // exit here to just test sonar
  } // end setup

void doTraining() {  
  episodes = 40;  
  for (int episode=0;episode<episodes;episode++) // no. of episodes 
  {
       
       state=random(16);           // randomly select a state 0 to 15
       if ( episode % 2 == 0) {    // even episode so load spos1 and spos2
          spos1 = pos[state][0];
          spos2 = pos[state][1];
          if (episode == 0) {   // first episode so need to move arm from starting position to state position
                               // if we dont do this then starting really starts from highest position and gives false distance reading
             //   spos1 = pos[state][0];
               // spos2 = pos[state][1];
                servo1.write(spos1,60,false); // move servo 1 - false means don't wait for move to finish before going to next instruction
                servo2.write(spos2,60,false);
                servo1.wait();                // now wait until servo finishes 
                servo2.wait();
               
          }
       }
       else                        // odd episode so load spos2 and spos3 and move servos, get distance and store successes in successes array
          { 
            spos3 = pos[state][0];
            spos4 = pos[state][1];

         
            servo1.write(spos1,60,false); // move servo 1 - false means don't wait for move to finish before going to next instruction
            servo2.write(spos2,60,false);
            servo1.wait();                // now wait until servo finishes 
            servo2.wait();
            
            servo1.write(spos3,60,false); // move 
            servo2.write(spos4,60,false);
            servo1.wait();
            servo2.wait();
          
            distCurrent = getDistance(); // get distance - note this is not always accurate so sometimes robot will just claw the air
            distDifference = distCurrent - distPrevious;
            distPrevious = distCurrent;
            
            Serial.print(" episode = ");Serial.print(episode);
            Serial.print(" state = ");Serial.print(state);
            Serial.print(" spos1 = ");Serial.print(spos1);
            Serial.print(" spos2 = ");Serial.println(spos2);
            Serial.print(" spos3 = ");Serial.print(spos3);
            Serial.print(" spos4 = ");Serial.println(spos4);
            Serial.print(" distance = ");Serial.println(distDifference);
            Serial.println(" ");
     
            if ( distDifference > 1.9) { // if moved forward 2 or more centimeters
               success[numberSuccesses][0] = spos1; // servo position 1
               success[numberSuccesses][1] = spos2; // servo position 2
               success[numberSuccesses][2] = spos3; // servo position 1
               success[numberSuccesses][3] = spos4; // servo position 2
               success[numberSuccesses][4] = distDifference; // store distance   
               numberSuccesses = numberSuccesses + 1;
               if (numberSuccesses > 14) episodes = 10000; // escape loop if successes array is full
               }

           } // end if mod 2
   
}  // end each episode

   Serial.print(" NumberSuccesses = ");Serial.println(numberSuccesses);
   for (int i=0;i<16;i++){  // print success table
     for(int j=0;j<5;j++){
       Serial.print(success[i][j]);
       Serial.print("  ");
     }
    Serial.println(" ");
   }
 
} // end doTraining

void getLongestStep() {
  Serial.println("Do getLongestStep...");
  servo1.write(0,20); // start at 0 state
  servo2.write(40,20);
  delay(2000);
  
  int prevDistance = 0; // local variables
  int currDistance = 0;
  int highDistance = 0;

  spos1 = 0;
  spos2 = 0;
  spos3 = 0;
  spos4 = 0;
  for(int i=0;i<16;i++){ // find highest distance and use those servo postions to move robot
      currDistance = success[i][4];
      if (currDistance != 0 && currDistance> prevDistance) {
         highDistance = currDistance;
         spos1 = success[i][0];
         spos2 = success[i][1];
         spos3 = success[i][2];
         spos4 = success[i][3];
      }
      prevDistance = currDistance;
  } // end while
} // end doTraining()

void doLearnedBehavior() {
     Serial.println("Do Learned behavior... ");
     servo1.write(0,30,false); //starting position for servo 1
     servo2.write(0,30,false);
     servo1.wait();
     servo2.wait();
     
     for (int i=0;i<10;i++) {
       Serial.print(" spos1 = ");Serial.print(spos1);
       Serial.print(" spos2 = ");Serial.println(spos2);
       Serial.print(" spos3 = ");Serial.print(spos3);
       Serial.print(" spos4 = ");Serial.println(spos4);
     

       servo1.write(spos1,50,false); // first servo positions
       servo2.write(spos2,50,false);
       servo1.wait();
       servo2.wait();
           
       servo1.write(spos3,50,false); // 2nd position
       servo2.write(spos4,50,false);
       servo1.wait();
       servo2.wait();
      
       state = state + 1;
  } // doLearned
  
} // end loop

void loop(){  // main loop does training, reads success table and performs actions
   doTraining();     // trial and error training with distance reinforcement
   getLongestStep(); // find servo positions for longest step
   doLearnedBehavior(); // do longest step n times to make robot crawl
   servo1.write(0,30,false); //return to starting position for servo 1
   servo2.write(0,30,false); //return to starting position for servo 2
   servo1.wait();
   servo2.wait();
   delay(2000);
   exit(0);  // quit program
    
} // end main loop

float getDistance() {  // routine to measure distance = call and average it
  int numberTriggers = 5;
  int average = 0;
  for(int i=0;i<numberTriggers;i++) {
     digitalWrite(TRIGGER, LOW);
     delayMicroseconds(5);
     digitalWrite(TRIGGER, HIGH);
     delayMicroseconds(10);
     digitalWrite(TRIGGER, LOW);
     sonarTime = pulseIn(ECHO, HIGH);
     distance = sonarTime / 58.00;
     average = average + distance;
     Serial.print(sonarTime);Serial.print(" ");
     Serial.print(distance);
     Serial.println("cm");
     delay(100);
  } // end for i
  average = average / numberTriggers;
return average;
}// end get sonar distance routine


