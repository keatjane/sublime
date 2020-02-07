import smbus,time,datetime, csv

class srf02:
  def __init__(self):
    self.i2c = smbus.SMBus(1)
    # Check address of sensor with i2cdetect -y 1 if unsure
    self.addr = 0x70
  
  def getValues(self):
    startTime = datetime.datetime.now()

    self.i2c.write_byte_data(self.addr, 0, 81)
    time.sleep(0.08) # 80ms snooze whilst it pings
    
    distance = self.i2c.read_word_data(self.addr, 2) / 255
    #mindistance = self.i2c.read_word_data(self.addr, 4) / 255
    time.sleep(0.12) # 120ms snooze so we only take 5 readings per second

    return distance

  def printValues(self):
    distance = self.getValues()
    print("%.3f" % (distance))

    with open('2m.csv', mode='a') as results:
      results = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      results.writerow([distance])
      
def main():
  foo = srf02()
  print("Range")
  while(1):
    try:
      foo.printValues()
    except KeyboardInterrupt:
      break

if __name__ == "__main__":
    main()
