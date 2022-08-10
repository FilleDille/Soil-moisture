from machine import ADC, Pin
import time
import tm1637

def main():
    tm = tm1637.TM1637(clk=Pin(1), dio=Pin(0))
    tm.brightness(0)
    analog_value = ADC(Pin(26))
    conversion_factor = 3.3 / (65535)
    measure_freq = 0.2
    measure_wait = 300
    measure_count = 100
    voltage_max = 1.90 # v when time to water
    voltage_min = 1.65 # v about one hour after watering
    

    while True:
        measure_list = []
        tm.show('CALC')
        
        for i in range(measure_count):
            analog_read = analog_value.read_u16()
            voltage_value = analog_read * conversion_factor
            measure_list.append((voltage_value - voltage_min) / (voltage_max - voltage_min))
            time.sleep(measure_freq)
        
        measure_list.sort()
        measure_median = 1 - measure_list[int(measure_count/2)]
        print(str(measure_median) + " " + str(voltage_value))
        
        if measure_median > 1:
            moist_index = " 100"
        elif measure_median < 0:
            moist_index = "   0"
        else:
            moist_index = "  " + str(measure_median).replace(".", "")[1:3]
        
        tm.show(moist_index, False)
        
        date_now = str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2])
        time_now = str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5])
        
        stats = open("stats.csv", "a")
        stats.write(date_now + "," + time_now + "," + moist_index.strip() + "\n")
        stats.close()
        
        time.sleep(measure_wait)

if __name__ == '__main__':
    main()
