import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial("/dev/ttyS0",115200)
ser.flushInput()

#message = input('Text: ')
#number = input('To: ')

#key the power for module is connected to
power_key = 6
#idk something to do with the response from the serial
rec_buff = ''

#send AT commands through serial
def send_at(command, expected_response, wait_time):
    ser.write((command+'\r\n').encode())
    time.sleep(wait_time)
    #if response from serial
    if ser.inWaiting():
        time.sleep(0.01)
        #read response
        rec_buff = ser.read(ser.inWaiting())
        print(rec_buff)
        try:
            if expected_response not in rec_buff.decode():
                print(command, 'Error')
                print(command + ' back:\t' + rec_buff.decode())
                return 'broken'
            else:
                print(rec_buff.decode())
                return rec_buff.decode()
        except:
            return False
    else:
        return False

def send_text(number, message):
    print('sending message')
    success = send_at(f'AT+CMGS="{number}"', '>', 2)
    if success:
        print('next bit')
        ser.write(message.encode())
        ser.write(b'\x1A')
        send_success = send_at('', 'OK', 20)
        if send_success:
            print('sent')
        else:
            print('send failed')
    else:
        print('error')
        
def read_all():
    print('requesting texts')
    messages = send_at('AT+CMGL="ALL"', '', 20)
    if messages:
        print('yay')
        return messages
    else:
        return False
    
def read_unread():
    print('requesting texts')
    messages = send_at('AT+CMGL="REC UNREAD"', '', 20)
    if messages:
        print('yay')
        return messages
    else:
        return False
        
def power_on(power_key):
    print('start power up')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('powered up')
    
def start_up():
    power_on(6)
    on = send_at('AT+COPS?', 'Telstra', 5)
    broken = False
    if on in (False, 'broken'):
        broken = True
    while broken:
        broken = False
        if on == 'broken':
            power_off(6)
            time.sleep(3)
            power_on(6)
        on = send_at('AT+COPS?', 'Telstra', 5)
        if on in (False, 'broken'):
            broken = True
    print('serial working and network available')
    send_at('AT+CMGF=1', 'OK', 5)
    print('in SMS mode')
    
def power_off(power_key):
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(3)
    GPIO.output(power_key,GPIO.LOW)
    print('powered off')
    
'''try:
    power_on(power_key)
    send_text(number, message)
    read_all()
    power_off(power_key)
    
except:
    print('oops')
    if ser != None:
        ser.close()
    GPIO.cleanup()'''
