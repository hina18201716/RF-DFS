import serial
import time

ser = serial.Serial( port = 'COM4', baudrate= 9600, bytesize= 8, parity='N', stopbits=1,xonxoff=0 ) 
print(ser.is_open)

# line = ser.readline()
# time.sleep(0.5)
# if line.decode('utf-8') == '':
#     print ( "no message" )
# else:
#     print(line.decode('utf-8'))

# ser.write('prog 0'.encode('utf-8'))
# ser.write(bytes(b'prog 0\r\n'))
def serialRead():
    line = ser.readline()
    print(line.decode('utf-8'))

drive = 'drive on x y\r\n'
jog = 'jog abs x 20\r\n'
printasdf = 'print asdf'


# time.sleep(0.5)
# ser.write('\r\n'.encode('utf-8'))
ser.write('print "asdf"\r\n'.encode('utf-8'))
print(type('print "asdf"\r\n'))
# time.sleep(1)
ser.write(b'drive on x y\r\n')
time.sleep(1)
ser.write(b'jog abs y 0\r\n')


time.sleep(1)
while True:
    serialRead()
    # ser.write('\r\n'.encode('utf-8'))
# ser.write(jog.encode('utf-8'))
# time.sleep(1)
# serialRead()
# ser.write('\r\n'.encode('utf-8'))
# ser.write('\r\n'.encode('utf-8'))


# line = ser.readline()
# time.sleep(0.5)
# if line.decode('utf-8') == '':
#     print ( "no message" )
# else:
#     print("message from motor: " + line.decode('utf-8'))

