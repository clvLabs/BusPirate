#!/usr/bin/python3 -u
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
import logging

from src.utils import *
from config import *

COMMENT_SYMBOL = "//"
BP_READY_SYMBOL = ">"
BP_BASICMODE_STR = "(BASIC)"

log = None
args = None

# Serial port
gSerial = serial.Serial()

def connect(port):
    global gSerial

    gSerial.port = port
    gSerial.baudrate = SERIAL_SPEED
    gSerial.timeout = SERIAL_TIMEOUT

    if(gSerial.isOpen()):
        gSerial.close()

    log.debug('--- Opening serial port')
    try:
        gSerial.open()
    except:
        pass

    if not gSerial.isOpen():
        log.error('!!! ERROR opening serial port, exiting program')
        quit()

    log.debug('--- Serial port open')
    resp = send("")
    if resp and BP_BASICMODE_STR in resp[-1]:
        log.debug('--- Exiting BASIC mode')
        send("exit")

def send(command):
    log.info(f">>> {command}")
    serialCommand = command + '\n'
    gSerial.write(serialCommand.encode())
    return waitresponse()

def waitresponse():
    startTime = time.time()
    lastRecTime = 0
    response = []

    while( True ):
        line = gSerial.readline()
        if(line):
            line = line.decode()
            response.append(line)
            lastRecTime = time.time()
            displine = line.replace('\n','')
            log.info(f"<<< {displine}")
            # Check if command was completed (response will be something like "HiZ>")
            if line[-1] == BP_READY_SYMBOL:
                break
    else:
        log.error('!!! Timeout waiting for response')

    return response

def resetBoard():
    log.debug('--- Resetting board')
    send('#')
    delay(RESET_DELAY)

def sendScript(file):
    data = open(file, encoding='utf8')
    lines = [line.replace('\n', '').strip() for line in data]
    log.debug(f'--- Sending script file ({file}) - {len(lines)} lines')

    for line in lines:
        line = line.strip()
        if line == '#':
            resetBoard()    # Correctly handle reset timeout
        else:
            parts = line.split(COMMENT_SYMBOL)
            command = parts.pop(0).strip()
            comments = COMMENT_SYMBOL.join(parts)
            if comments:
                log.debug(f"/// {comments}")
            if command == '':
                delay(SCRIPT_BLANK_LINE_DELAY)
            else:
                send(command)

def main():
    global log
    global args

    programStartTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('scriptFileName', nargs='?', help='set script file to use (default: {:s})'.format(SCRIPT_FILE), default=SCRIPT_FILE)
    parser.add_argument('-c', '--comPort', help='set COM port (default: {:s})'.format(SERIAL_PORT), default=SERIAL_PORT)
    parser.add_argument('-l', '--logmode', action="store_true", help='log mode', )

    args = parser.parse_args()

    if args.logmode:
        logging.basicConfig(
            stream=sys.stdout,
            format='%(asctime)s.%(msecs)03d %(message)s',
            level=logging.INFO,
            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.basicConfig(
            stream=sys.stdout,
            format='%(message)s',
            level=logging.DEBUG)

    log = logging.getLogger("buspirate")

    log.debug('--- Bus Pirate scripting tool')
    log.debug(f'--- Script file: {args.scriptFileName}')
    log.debug(f'--- COM port: {args.comPort}')
    log.debug(f'--- Log mode: {args.logmode}')

    connect(args.comPort)

    if RESET_AT_STARTUP:
        resetBoard()

    sendScript(args.scriptFileName)

    if RESET_AT_END:
        resetBoard()

    log.debug('--- Closing serial port')
    gSerial.close()
    log.debug(f"--- Finished in {time.time() - programStartTime:.2f} seconds")


if __name__ == '__main__':
    main()
