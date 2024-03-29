# BusPirate

A simple scripting tool for Bus Pirate written in Python.

It allows you to save your *scripts* in text files, using the same syntax you are using in the terminal, and showing the same results.

Can be used as an automation tool when you need to do repetitive tasks with your Bus Pirate, or simply to keep a list of useful scripts (e.g. basic testing of LCD screens)

```
$ ./buspirate.py scripts/sample.txt
--- Bus Pirate scripting tool
--- Script file: scripts/sample.txt
--- COM port: /dev/ttyUSB0
--- Log mode: False
--- Opening serial port
--- Serial port open
>>>
<<<
<<< HiZ>
--- Resetting board
>>> #
<<< #
<<< RESET
<<<
<<< Bus Pirate v3b
<<< Firmware v5.10 (r559)  Bootloader v4.4
<<< DEVID:0x0447 REVID:0x3046 (24FJ64GA002 B8)
<<< http://dangerousprototypes.com
<<< HiZ>
--- Sending script file (scripts/sample.txt) - 10 lines
///  set I2C mode
>>> m4
<<< m4
<<< Set speed:
<<<  1. ~5KHz
<<<  2. ~50KHz
<<<  3. ~100KHz
<<<  4. ~400KHz
<<<
<<< (1)>
///  set I2C speed (400KHz)
>>> 4
<<< 4
<<< Ready
<<< I2C>
///  start power supplies
>>> W
<<< W
<<< Power supplies ON
<<< I2C>
///  read pin states
>>> v
<<< v
<<< Pinstates:
<<< 1.(BR)	2.(RD)	3.(OR)	4.(YW)	5.(GN)	6.(BL)	7.(PU)	8.(GR)	9.(WT)	0.(Blk)
<<< GND	3.3V	5.0V	ADC	VPU	AUX	SCL	SDA	-	-
<<< P	P	P	I	I	I	I	I	I	I
<<< GND	3.24V	4.96V	0.00V	0.00V	L	L	L	L	L
<<< I2C>
///  read voltage probe
>>> d
<<< d
<<< VOLTAGE PROBE: 0.00V
<<< I2C>
///  delay
///  stop power supplies
>>> w
<<< w
<<< Power supplies OFF
<<< I2C>
///  read pin states
>>> v
<<< v
<<< Pinstates:
<<< 1.(BR)	2.(RD)	3.(OR)	4.(YW)	5.(GN)	6.(BL)	7.(PU)	8.(GR)	9.(WT)	0.(Blk)
<<< GND	3.3V	5.0V	ADC	VPU	AUX	SCL	SDA	-	-
<<< P	P	P	I	I	I	I	I	I	I
<<< GND	0.00V	0.02V	0.00V	0.00V	L	L	L	L	L
<<< I2C>
///  read voltage probe
>>> d
<<< d
<<< VOLTAGE PROBE: 0.00V
<<< I2C>
///  set HiZ mode
>>> m1
<<< m1
<<< Ready
<<< HiZ>
--- Closing serial port
```

* Lines starting with `---` are informational messages
* Lines starting with `///` are comments
* Lines starting with `>>>` are sent messages
* Lines starting with `<<<` are received messages

It uses the [basic text mode](http://dangerousprototypes.com/docs/Bus_Pirate_menu_options_guide) used for terminal access, **not** the [bitbang protocol](http://dangerousprototypes.com/docs/Bitbang). This makes the tool not suitable for timing-strict applications, for those kind of scripts you will have to find yourself a *bitbanging library* ([see here](http://dangerousprototypes.com/docs/Bus_Pirate_Scripting_in_Python))

## How to install it

* Make sure you have [python 3](https://www.python.org/downloads/) installed
* Clone this repo (or download and extract the .zip file)
* If running on Linux, make sure you `chmod -x buspirate.py`
* Open `config.py` with your favorite text editor to change default settings.

### config.py

```
SERIAL_PORT = '/dev/ttyUSB0'
RESET_AT_STARTUP = True
RESET_AT_END = False
SCRIPT_BLANK_LINE_DELAY = 250
```

* `SERIAL_PORT`: default serial port name (Use `COMx` on Windows)
* `RESET_AT_STARTUP`: if `True` the board is always reset before processing a script
* `RESET_AT_END`: if `True` the board is always reset after processing a script
* `SCRIPT_BLANK_LINE_DELAY`: milliseconds to *sleep* when a blank line is found

## How to use it

### Syntax

```
usage: buspirate.py [-h] [-c COMPORT] [-l] scriptFileName

positional arguments:
  scriptFileName        set script file to use

optional arguments:
  -h, --help            show this help message and exit
  -c COMPORT, --comPort COMPORT
                        set COM port (default: /dev/ttyUSB0)
  -l, --logmode         log mode
```

### Quick tryout
`./buspirate.py scripts/sample.txt`

This will connect to the bus pirate in `[SERIAL_PORT]` and run the sample script provided with the project (the one in the screenshot).


### Logging mode
`./buspirate.py scripts/sample.txt -l`

When `-l` or `--logmode` is specified:
* A timestamp is added to each line
* Only transmitted errors and log messages are displayed

```
2020/10/09 00:40:09.211 >>>
2020/10/09 00:40:09.221 <<<
2020/10/09 00:40:09.321 <<< HiZ>
2020/10/09 00:40:09.322 >>> #
2020/10/09 00:40:09.351 <<< #
2020/10/09 00:40:09.351 <<< RESET
2020/10/09 00:40:09.351 <<<
2020/10/09 00:40:09.351 <<< Bus Pirate v3b
2020/10/09 00:40:09.352 <<< Firmware v5.10 (r559)  Bootloader v4.4
2020/10/09 00:40:09.352 <<< DEVID:0x0447 REVID:0x3046 (24FJ64GA002 B8)
2020/10/09 00:40:09.353 <<< http://dangerousprototypes.com
...
```

## Sample scripts

See the [scripts](scripts) folder.
