# BusPirate sample scripts

Some sample scripts are provided, but the key to make this program useful is to create your own scripts. You can use the `scripts/` folder to store them.

Comments can be added using `//` and will be displayed on program output.

## sample.txt

This is the default script configured to be executed if none is specified in the command line.

This script does not need anything connected to your Bus Pirate.

```
m4      // set I2C mode
4       // set I2C speed (400KHz)
W       // start power supplies
v       // read pin states
d       // read voltage probe
        // delay
w       // stop power supplies
v       // read pin states
d       // read voltage probe
m1      // set HiZ mode
```

## reset.txt

This script resets your board.

It is an empty file, so it relies in your configuration having `RESET_AT_STARTUP` or `RESET_AT_END` set to `True`.

If you want to have both of them set to `False` in your configuration, edit `reset.txt` script and add a '#' character, which is the Bus Pirate *reset* command.

## lcd.txt

This scripts does a simple test on a 2-line [HD44780 compatible LCD screen](https://www.sparkfun.com/datasheets/LCD/HD44780.pdf) (**PDF warning**) using a [Bus Pirate LCD adapter](http://dangerousprototypes.com/docs/Bus_Pirate_v3_LCD_adapter).

```
m8                    // set LCD mode
W                     // start power supplies
(1)                   // reset LCD
(2)                   // init LCD
2                     // set number of lines (2)
(3)                   // clear LCD
(4) 0  "Bus Pirate"   // set cursor to 0 and write text
(4) 40 "LCD test"     // set cursor to 40 (line 2) and write text
```

**NOTE**: This script does **not** reset the board to *HiZ* mode at the end to keep the display ON with the message. To stop the LCD screen you can use the `reset` script.

## rtc.txt

This scripts reads the date and time from a [DS1307 RTC](https://datasheets.maximintegrated.com/en/ds/DS1307.pdf) (**PDF warning**) via I2C.

```
m4                             // set I2C mode
3                              // set I2C speed (100KHz)
W                              // start power supplies
[ 0xd0 0x00 [ 0xd1 rrrrrrr ]   // read 7 bytes from addr 0xd1 reg 0x00
w                              // stop power supplies
m1                             // set HiZ mode
```

## adcread.txt

This script reads the ADC pin 5 times with 20ms between reads and prints out results.
It is an example on how [Bus Pirate BASIC](http://dangerousprototypes.com/docs/Bus_Pirate_BASIC_script_reference) code can be used to create more complex scripts.

(Courtesy of [PSLLSP@github](https://github.com/PSLLSP), thanks mate!)

```
s                         // Enter the script engine
new                       // Create a new BP BASIC script:
10 AUX 1                  // - Set AUX pin HIGH
20 FOR I=1 TO 5           // - Repeat 5 times:
30 LET A=ADC              //     - Get value from ADC pin into A
40 PRINT I;": ";A         //     - Print iteration number and ADC value
50 DELAY 20               //     - Wait 20ms
60 NEXT I                 //     - Increment iteration counter
70 AUX 0                  // - Set AUX pin LOW
80 PRINT "WORK DONE"      // - Print finished message
list                      // Show the script listing
run                       // Run the script
exit                      // Exit the script engine
```

The output is something like this:
```
***[ Bus Pirate scripting tool ]********************************************************************
Script file                             adcread.txt
COM port                                /dev/ttyUSB0
- Opening serial port
[OK] Serial port open
- Resetting board
>>> ------------------------------------| #
<<< #
<<< RE
<<< Bus Pirate v3.b clone w/different PIC
<<< Firmware v6.3-beta1 r2151  Bootloader v4.4
<<< DEVID:0x044F REVID:0x3003 (24FJ64GA004 A3)
<<< http://dangerousprototypes.com
<<< HiZ>
- Sending script file (adcread.txt) - 13 lines
>>> ------------------------------------| s
<<< s
<<< HiZ(BASIC)>
>>> ------------------------------------| new
<<< new
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 10 AUX 1
<<< 10 AUX 1
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 20 FOR I=1 TO 5
<<< 20 FOR I=1 TO 5
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 30 LET A=ADC
<<< 30 LET A=ADC
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 40 PRINT I;": ";A
<<< 40 PRINT I;": ";A
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 50 DELAY 20
<<< 50 DELAY 20
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 60 NEXT I
<<< 60 NEXT I
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 70 AUX 0
<<< 70 AUX 0
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| 80 PRINT "WORK DONE"
<<< 80 PRINT "WORK DONE"
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| list
<<< list
<<<
<<< 10  AUX 1
<<< 20  FOR I=1 TO 5
<<< 30  LET A= ADC
<<< 40  PRINT I;": ";A
<<< 50  DELAY 20
<<< 60  NEXT I
<<< 70  AUX 0
<<< 80  PRINT "WORK DONE"
<<< 65535  END
<<< 67 bytes.
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| run
<<< run
<<< 1: 388
<<< 2: 387
<<< 3: 387
<<< 4: 387
<<< 5: 424
<<< WORK DONE
<<<
<<< Ready
<<< HiZ(BASIC)>
>>> ------------------------------------| exit
<<< exit
<<< Ready
<<< HiZ>
- Closing serial port
```
