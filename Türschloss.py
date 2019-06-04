#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Türschloss: Simulates opening an door on raspberrypi

import RPi.GPIO as GPIO
import time
import sys

# path and name of the log file
logfile = 'logfile.log'

# global vaiable to save stings for logfile
userName = " "
keyNr = " "

# function to save log messages to specified log file
def log(msg):
    try:
        # open the specified log file
        file = open(logfile,"a")
    except:
        print("Fehler beim öffnen von logfile.log")

    try:
        # write log message with timestamp to log file
        file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
    except:
        print("Fehler beim schreiben in logfile.log")
    finally:
        # close log file
        file.close

class AuthToken:
    def __init__(self, id, secret):
            self.id=id
            self.secret=secret

# class to let an led turn on to simulate an open door
class TestDoorController:
    def send_open_pulse(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)
        print ("Green LED on")
        GPIO.output(18,GPIO.HIGH)
        time.sleep(3)
        print ("Green LED off")
        GPIO.output(18,GPIO.LOW)

# class to let an led turn on to simulate an false login
class WrongLogin:
    def send_red_led(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(19,GPIO.OUT)
        print ("Red LED on")
        GPIO.output(19,GPIO.HIGH)
        time.sleep(3)
        print ("Red LED off")
        GPIO.output(19,GPIO.LOW)

# class for RFID Authentication
class RFIDFileAuthenticator:
    filename = "users.txt"
    tags = dict()
    def __init__(self):
        self.readFile()
    
    # read users.txt
    def readFile(self):
        try:
            secrets = open(self.filename, 'r')
        except:
            print("Fehler beim lesen von users.txt")        
        print("Lese Datei " +self.filename)
        for line in secrets:
            line = line.rstrip('\n')
            id, tag = line.split(',')
            self.tags[tag] = id
    
    # RFID token check
    def check(self,token):
        print("Prüfe ob " + token.secret + " gültig ist")
        if token.secret in self.tags:
            print("Transponder gehört: " + self.tags[token.secret])
            global userName
            global keyNr
            userName = str(self.tags[token.secret])
            keyNr = str(token.secret)
            return True
        else:
            print("Transponder-ID nicht gefunden")
            return False

# class for usb RFID serial reader
class RFIDInput:
    def getInput(self):
        print ("Auf Transponder warten")
        try:
            tag = input()
            tag=int(tag)
        except:
            print("Fehler bei der RFID Eingabe")
        
        return AuthToken(None,tag)

# main() running in an endless while loop
def main():
    while True:
        authInput = RFIDInput()
        authenticator = RFIDFileAuthenticator()
        doorController = TestDoorController()
        ledController = WrongLogin()
        if(authenticator.check(authInput.getInput())):
            doorController.send_open_pulse()
        else:
            ledController.send_red_led()                
        log(userName + "," + keyNr)

if __name__ == "__main__":
    main()