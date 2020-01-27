import time
import pigpio
import csv

BUS=1
SRF02_I2C_ADDR=0x70
SLEEP=0.07 #(sec), 読み取りに必要な最低時間は65msec(0.065sec)

def srf02_read(h):
   # レジスタ 0x02, 0x03 の値を読み取る
   high = pi.i2c_read_word_data(h,0x02)
   low = pi.i2c_read_word_data(h,0x03)

   ll=int(bin(low&0b1111111),2)  # lowの下位7bitを抜き出して10進に変換
                                 # 0-128cmの値が入る．
   lh=int(bin(low>>15),2)  # lowを15bit右にシフトして10進に変換
                           # 128-255cmの時に0b1になる
   hl=int(bin(high&0b11),2)  # highの下位2bitを抜き出す
                             # 256cm:0b01, 512cm:0b10
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
         print (d, 'cm') #minua 1.5 for height of sensor
         with open('0.5-2m.csv', mode='a') as results:
            results = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            results.writerow([d])
 	
      except KeyboardInterrupt:
         break

   pi.i2c_close(h)

print("\nTidying up")

pi.stop()
