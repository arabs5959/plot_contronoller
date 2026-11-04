from machine import PWM, Pin
import time
from servo_translator import translate 
start_point = 1
x_value = 0.0
y_value = 0.0
M = 0
file_path = "circle.gcode"




def read_gcode (file_path):
    global start_point, x_value, y_value, M
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line.startswith('G1'):
                parts = line.split()
                print("[Debug] parts = ", parts)
                x_value = None
                y_value = None
                for part in parts:
                    if part.startswith('S'):
                        x_value = float(part[1:])
                    elif part.startswith('E'):
                        y_value = float(part[1:])
                if x_value != 0.00 and y_value != 0.00:
                    print(f"Line {line_num}: X =", translate(x_value), "Y =", translate(y_value))
                    duty_cycle_x = translate(x_value)
                    duty_cycle_y = translate(y_value)
            if line.startswith('M'):
                if 'M3' in line:
                    print(f"Line {line_num}: M =", translate(30))

                    start_point = start_point + 1
                    
                if 'M5' in line:
                    print(f"Line {line_num}: M =", translate(0))
                    
                if 'M18' in line:
                    print(f"Line {line_num}: M =", translate(18))
    return
read_gcode(file_path)
# Initialize servos
def setup_servos():
    shoulder_servo = PWM(Pin(0))
    elbow_servo = PWM(Pin(1))
    pen_servo = PWM(Pin(2))

    shoulder_servo.freq(50)
    elbow_servo.freq(50)
    pen_servo.freq(50)

    return shoulder_servo, elbow_servo, pen_servo