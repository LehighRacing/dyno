#include "ADS1256.h"

// Pin configuration for Arduino UNO
#define ADS1256_PIN_CS      (10)
#define ADS1256_PIN_DRDY    (9)
#define ADS1256_PIN_RST     (8)


ADS1256 adc = ADS1256(ADS1256_PIN_CS, ADS1256_PIN_DRDY, ADS1256_PIN_RST);

void setup()
{
    // Setup serial
    Serial.begin(115200);

    Serial.println("Initializing...");

    // Setup pins and initialize the ADS1256 chip
    adc.begin();

    // Configure reading a differential between AIN0 and AIN1
    adc.SetMux(ADS1256_MUX_AIN0, ADS1256_MUX_AIN1);

    // For now, refer to the datasheet
    adc.WriteRegister(ADS1256_REG_ADCON, 0b00100111);
    adc.WriteRegister(ADS1256_REG_DRATE, 0b00100011);

    Serial.println("Complete!");

    adc.StartReadDataContinuous();
}

#define CALIB_SMALL_PLATES (0)

#if CALIB_SMALL_PLATES
#define CALIB_OFFSET (64000)
#define CALIB_PER_LB (82000 / 8.3)
#else
#define CALIB_OFFSET (330000)
#define CALIB_PER_LB (180000 / 8.3)
#endif

void loop()
{
    unsigned long t = millis();
    int32_t value = 0;
    adc.ShiftOutData(&value);

    Serial.print(t);
    Serial.print(" ");
    Serial.println((value - CALIB_OFFSET) / float(CALIB_PER_LB), 6);

    Serial.flush(); // Ensure the data has been transmitted
}
