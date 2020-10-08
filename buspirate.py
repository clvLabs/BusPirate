#!/usr/bin/env python3
# coding=utf-8

"""
Bus Pirate scripting tool
"""

import sys
import os
import pathlib
import argparse
import time
import serial

from src.utils import *
from config import *

COMMENT_SYMBOL = "//"
BP_READY_SYMBOL = ">"
BP_BASICMODE_STR = "(BASIC)"

# Serial port
gSerial = serial.Serial()

def connect(port):
    global gSerial

    gSerial.port = port
    gSerial.baudrate = SERIAL_SPEED
    gSerial.timeout = SERIAL_TIMEOUT

    if(gSerial.isOpen()):
        gSerial.close()

    showMsg('Opening serial port')
    try:
        gSerial.open()
    except:
        pass

    if not gSerial.isOpen():
        showErrorMsg('ERROR opening serial port, exiting program')
        quit()

    showOKMsg('Serial port open')
    resp = send("")
    if resp and BP_BASICMODE_STR in resp[-1]:
        showMsg('Exiting BASIC mode')
        send("exit")

def send(command):
    showSentMsg(command)
    serialCommand = command + '\n'
    gSerial.write(serialCommand.encode())
    return waitresponse()

def waitresponse():
    startTime = time.time()
    lastRecTime = 0
    response = []

    while( (time.time() - startTime) < (SERIAL_RESPONSE_TIMEOUT/1000) ):
        line = gSerial.readline()
        if(line):
            line = line.decode()
            response.append(line)
            lastRecTime = time.time()
            showReceivedMsg(line)
            # Check if command was completed (response will be something like "HiZ>")
            if line[-1] == BP_READY_SYMBOL:
                break
        else:
            if lastRecTime:
                diff = (time.time() - lastRecTime) * 1000
                if diff > SERIAL_RESPONSE_END_SILENCE:
                    break
    else:
        showErrorMsg('Timeout waiting for response')

    return response

def resetBoard():
    showMsg('Resetting board')
    send('#')
    delay(RESET_DELAY)

def sendScript(file):
    data = open(file, encoding='utf8')
    lines = [line.replace('\n', '').strip() for line in data]
    numLines = len(lines)
    showMsg('Sending script file ({0}) - {1} lines'.format(file, numLines))

    for line in lines:
        line = line.strip()
        if line == '#':
            resetBoard()    # Correctly handle reset timeout
        else:
            parts = line.split(COMMENT_SYMBOL)
            command = parts.pop(0).strip()
            comments = COMMENT_SYMBOL.join(parts)
            if comments:
                showCommentMsg(comments)
            if command == '':
                delay(SCRIPT_BLANK_LINE_DELAY)
            else:
                send(command)

def main():
    showTitle('Bus Pirate scripting tool', line='*', color='blue+')
    programStartTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('scriptFileName', nargs='?', help='set script file to use (default: {:s})'.format(SCRIPT_FILE), default=SCRIPT_FILE)
    parser.add_argument('-c', '--comPort', help='set COM port (default: {:s})'.format(SERIAL_PORT), default=SERIAL_PORT)

    args = parser.parse_args()

    showData('Script file', args.scriptFileName)
    showData('COM port', args.comPort)

    connect(args.comPort)

    if RESET_AT_STARTUP:
        resetBoard()

    sendScript(args.scriptFileName)

    if RESET_AT_END:
        resetBoard()

    showMsg('Closing serial port')
    gSerial.close()


if __name__ == '__main__':
    try:
        main()
    except:
        print()
        print()
        print('----------------------------------------------')
        print('An error happened, execution interrupted:')
        print(sys.exc_info())
