import datetime
import random

def header():
    return bytearray([0xAA,0xBB])
    
def footer():
    return bytearray([0xAA,0xCC])

def nowtime(sendNow):
    sendYear = sendNow.year -1911
    sendMonth = sendNow.month
    sendDay = sendNow.day
    sendHour = sendNow.hour
    sendMinute = sendNow.minute
    sendSecond = sendNow.second
    return bytearray([ sendYear, sendMonth, sendDay, sendHour, sendMinute, sendSecond])

def cks(command):
    cks = 0
    for i in range(len(command)):
        cks =cks ^ command[i]
    return cks
    
def inArea(sendNow):
    inA = sendNow - datetime.timedelta(seconds= random.randint(30,60))
    inA_year = inA.year-1911 
    inA_month = inA.month 
    inA_day = inA.day 
    inA_hour = inA.hour
    inA_min= inA.minute
    inA_sec = inA.second
    return bytearray([ inA_year, inA_month, inA_day, inA_hour, inA_min, inA_sec])
	
def outArea(sendNow):
    outA = sendNow - datetime.timedelta(seconds= random.randint(30,60))
    outA_year = outA.year-1911
    outA_month = outA.month
    outA_day = outA.day
    outA_hour = outA.hour
    outA_min= outA.minute
    outA_sec = outA.second
    return bytearray([ outA_year, outA_month, outA_day, outA_hour, outA_min, outA_sec])
    

def command33(addr,seq):
    sendNow = datetime.datetime.now()
    DeliverTime = nowtime(sendNow)
    commandLength = 10 +9
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xDF,0x33]) + DeliverTime + bytearray([0]) + footer()
    command.append(cks(command))
    return command

def commandB0(addr,seq):
    sendNow = datetime.datetime.now()
    DeliverTime = nowtime(sendNow)
    Amount = 2
    multiCar = bytearray()
    for i in range(Amount):
        LaneNo = random.randint(1,30)
        CarID = random.randint(1,10000)
        CarID = CarID.to_bytes(2,'big')
        CarType = random.randint(1,5)
        TurnNolist =[0,4,6,100,102,96,64,68,70,32,36,34,38,17,19,21,23,113,115,117,119,81,83,85,87,49,51,53,55]
        TurnNo = random.choice(TurnNolist)    
        TurnNo = TurnNo.to_bytes(2,'big')    
        InTime = inArea(sendNow)
        OutTime = outArea(sendNow)
        multiCar += bytearray([LaneNo])+ CarID + bytearray([CarType]) +TurnNo + InTime + OutTime


    commandLength = 10 + 9 +18 * Amount
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xDF,0xB0]) + DeliverTime + bytearray([Amount]) + multiCar + footer()
    command.append(cks(command))
    return command

def commandB1(addr,seq):
    sendNow = datetime.datetime.now()
    DeliverTime = nowtime(sendNow)
    DectectNo = random.choice([1,1,1,3])
    print(DectectNo)
    CarID = random.randint(1000,1001)
    print(CarID)
    CarID = CarID.to_bytes(2,'big')
    CarType = random.choice([50,80,112])
    InTime = inArea(sendNow)
    OutTime = outArea(sendNow)

    commandLength = 10 + 25
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xDF,0xB1])+ DeliverTime +  bytearray([0x01,DectectNo]) +CarID + bytearray([CarType]) + InTime + OutTime + footer()
    command.append(cks(command))
    return bytes(command)
    
def commandB2(addr,seq):
    sendNow = datetime.datetime.now()
    DeliverTime = nowtime(sendNow)
    DectectNo = random.randint(1,30)
    CarID = random.randint(1,10000)
    CarID = CarID.to_bytes(2,'big')
    CarType = random.randint(1,5)
    InTime = inArea(sendNow)
    OutTime = outArea(sendNow)

    commandLength = 10 + 24
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xDF,0xB2])+ DeliverTime + bytearray([DectectNo]) +CarID + bytearray([CarType]) + InTime + OutTime + footer()
    command.append(cks(command))
    return command

def commandAF11(addr,seq):
    commandLength = 10 + 3
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xAF,0x11]) + textID.to_bytes(1,'big') + footer()
    command.append(cks(command))
    return bytes(command)


def commandAF13(addr,seq, textID):
    commandLength = 10 + 3
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xAF,0x13]) + textID.to_bytes(1,'big') + footer()
    command.append(cks(command))
    return bytes(command)

def commandAF41(addr,seq, textID):
    commandLength = 10 + 3
    command = header() + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') + bytearray([0xAF,0x41]) + textID.to_bytes(1,'big') + footer()
    command.append(cks(command))
    return bytes(command)



def commandAck(addr,seq):
    commandLength = 8
    command = bytearray([0xAA,0xDD]) + seq.to_bytes(1,'big') + addr.to_bytes(2,'big') + commandLength.to_bytes(2,'big') 
    command.append(cks(command))
    return command