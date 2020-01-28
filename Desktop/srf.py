import time
import pigpio
import csv

BUS=1
SRF02_I2C_ADDR=0x70
SLEEP=0.07 #(sec), Minimum reading time is 65msec(0.065sec)

def srf02_read(h):
   # Reading value of 0x02, 0x03 
   high = pi.i2c_read_word_data(h,0x02)
   low = pi.i2c_read_word_data(h,0x03)

   ll=int(bin(low&0b1111111),2)  # Extract the lower 7 bits of low and convert to decimal
                                 # Enter the value of 0-128cm
   lh=int(bin(low>>15),2)  # Shift low to right by 15 bits and convert to decimal
                           # 0b1 at 128-255cm
   hl=int(bin(high&0b11),2)  # Extract the lower 2 bits of high
                             # 256cm: 0b01, 512cm: 0b10
   d =hl*255+lh*128+ll
   return d

def srf02_fake_mesure(h):
   pi.i2c_write_device(h,[0x00,0x57]);

def srf02_burst(h):
   pi.i2c_write_device(h,[0x00,0x5C]);

def srf02_mesure(h):
   pi.i2c_write_device(h,[0x00,0x51]);

pi = pigpio.pi()

if not pi.connected:
   exit()

h = pi.i2c_open(BUS, SRF02_I2C_ADDR)

if h>=0:
   while(1):

      try:
         srf02_mesure(h)
         time.sleep(SLEEP)
         d=srf02_read(h)
         print (d, 'cm') #minum 1.5 for height of sensor
         with open('0.5-2m.csv', mode='a') as results:
            results = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            results.writerow([d])
 	
      except KeyboardInterrupt:
         break

   pi.i2c_close(h)

print("\nTidying up")

pi.stop()
