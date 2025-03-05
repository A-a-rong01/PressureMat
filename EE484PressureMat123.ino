#define USE_ESP32 true  // Adjusts for ESP32 ADC scaling

// Secondary MUX (selects which primary MUX is active)
const int secRowMuxS[4] = {18, 5, 4, 2};  // Secondary row MUX select pins
const int secColMuxS[4] = {22, 23, 21, 19}; // Secondary column MUX select pins

// Primary MUX (connected to the secondary MUX)
const int priRowMuxS[4] = {13, 12, 15, 14}; // Primary row MUX select pins
const int priColMuxS[4] = {32, 27, 26, 25}; // Primary column MUX select pins

const int rowMuxOut = 33;  // Pin Power output to row (via MOSFET) 
const int colMuxIn = 34;   // Pin Analog input for columns

const int rows = 9; //change these to 44x44
const int cols = 9;
int sensorValues[rows][cols];

void setup() {
    Serial.begin(115200);

    // Set secondary and primary MUX control pins as outputs
    for (int i = 0; i < 4; i++) {
        pinMode(secRowMuxS[i], OUTPUT);
        pinMode(secColMuxS[i], OUTPUT);
        pinMode(priRowMuxS[i], OUTPUT);
        pinMode(priColMuxS[i], OUTPUT);
    }
    pinMode(rowMuxOut, OUTPUT);
}

void loop() {
    readPressureMat();
    sendHeatmapData();
    delay(800);
}

void readPressureMat() {
    for (int r = 0; r < rows; r++) {
        int primaryMux = r / 16;  // Select which primary MUX (0, 1, or 2)
        int channel = r % 16;      // Select channel within the MUX
       // Serial.print("PrimaryMux ");
       // Serial.println(primaryMux);
        setMux(secRowMuxS, primaryMux); // Select active primary row MUX
       // Serial.print("Test Row ");
        //Serial.println(r);
        setMux(priRowMuxS, channel);    // Select row within MUX
        digitalWrite(rowMuxOut, HIGH);  // Power row
      
        for (int c = 0; c < cols; c++) {
           // Serial.print("Test Col ");
           // Serial.print(c);
           // Serial.print(" ");
            int primaryMuxCol = c / 16; // Select primary column MUX
            int channelCol = c % 16;    // Select column within MUX

            setMux(secColMuxS, primaryMuxCol); // Select active primary col MUX
            setMux(priColMuxS, channelCol);    // Select column within MUX
            
            delayMicroseconds(800);
            int rawValue = analogRead(colMuxIn);
            
              sensorValues[r][c] = rawValue;
        }

        digitalWrite(rowMuxOut, LOW); // Turn off row to prevent ghosting
    }
}

// Function to control multiplexers
void setMux(const int muxPins[4], int channel) {
    for (int i = 0; i < 4; i++) {
        digitalWrite(muxPins[i], (channel >> i) & 1);
       // Serial.print((channel >> i) & 1, BIN);
        //Serial.print(" ");
    }
   // Serial.println();

}

// Send matrix data over serial
void sendHeatmapData() {
    Serial.println("START");
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            Serial.print(sensorValues[r][c]);
            if (c < cols - 1) Serial.print(",");
        }
        Serial.println();
    }
    Serial.println("END");
}
