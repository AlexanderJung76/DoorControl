#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Türschloss: Simulates opening an door on raspberrypi

import RPi.GPIO as GPIO
import time
import sys

# path and name of the log file
logfile = 'logfile.log'

# function to save log messages to specified log file
def log(msg):
  # open the specified log file
  file = open(logfile,"a")
  # write log message with timestamp to log file
  file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
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
        print ("LED on")
        GPIO.output(18,GPIO.HIGH)
        time.sleep(3)
        print ("LED off")
        GPIO.output(18,GPIO.LOW)

# class for RFID Authentication
class RFIDFileAuthenticator:
    filename = "users.txt"
    tags = dict()
    def __init__(self):
        self.readFile()
    
    # read users.txt
    def readFile(self):
        secrets = open(self.filename, 'r')
        print("Lese Datei " +self.filename)
        for line in secrets:
            line = line.rstrip('\n')
            id, tag = line.split(',')
            self.tags[tag] = id
    
    # RFID token check
    def check(self,token):
        print("Prüfe ob " + token.secret + " gültig ist")
        if token.secret in self.tags:
            print("Transport gehört: " + self.tags[token.secret])
            return True
        else:
            print("Transponder-ID nicht gefunden")
            return False

""" # test class for keybord input authentification
class FileAuthenticator:
    filename = "users.txt"
    def readFile(self):
        secrets = open(self.filename, 'r')
        print ("Datei einlesen")
        for line in secrets:
            line = line.rstrip('\n')
            self.id, self.secretPassword = line.split(',')

    def check(self,token):
        self.readFile()
        print("Eingabe für '" + token.id + "' Kennwort: '" + token.secret + "' wird mit geheimen Kennwort '" + self.secretPassword + "'verglichen")
        result = (token.secret == self.secretPassword) & (token.id == self.id)
        print("Authentifizierung ist: " +str(result))
        return result
 """

# class for usb RFID serial reader
class RFIDInput:
    def getInput(self):
        print ("Auf Transponder warten")
        tag = input()
        return AuthToken(None,tag)

""" # test class for keybord input
class KeybordInput:
    def getInput(self):
        print ("Eingabe prüfen")
        id = input("Bitte Namen eingeben: ")
        password = input("Bitte Kennwort eingeben: ")
        authToken = AuthToken(id, password)
        return authToken
 """        

# main() running in an endless while loop
def main():
    while True:
        authInput = RFIDInput()
        authenticator = RFIDFileAuthenticator()
        doorController = TestDoorController()
        if(authenticator.check(authInput.getInput())):
            doorController.send_open_pulse()
        log(self.id + "," + self.secret)
        #log("Token benutzt")

if __name__ == "__main__":
    main()