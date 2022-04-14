import serial, time
arduino = serial.Serial('COM3', 9600, timeout=.1)
time.sleep(1) #give the connection a second to settle
arduino.write("ON".encode())
time.sleep(1) #give the connection a second to settle
arduino.write("OFF".encode())
time.sleep(1) #give the connection a second to settle
arduino.write("ON".encode())
time.sleep(1) #give the connection a second to settle
arduino.write("OFF".encode())
time.sleep(1) #give the connection a second to settle
arduino.write("ON".encode())
time.sleep(1) #give the connection a second to settle
arduino.write("OFF".encode())
time.sleep(1) #give the connection a second to settle