import sys
import time

DISPLAY_MAXWIDTH = 100
DISPLAY_DATA_TITLE_PADDING = 40

# Give a string some ANSI color formatting
def colorStr(string, foreColor, backColor='black'):
    attr = []

    if foreColor.find('+'):
        foreColor = foreColor.replace('+','')
        attr.append('1')    # bright

    if foreColor == 'black':    attr.append('30')
    elif foreColor == 'red':    attr.append('31')
    elif foreColor == 'green':  attr.append('32')
    elif foreColor == 'yellow': attr.append('33')
    elif foreColor == 'blue':   attr.append('34')
    elif foreColor == 'magenta':    attr.append('35')
    elif foreColor == 'cyan':   attr.append('36')
    elif foreColor == 'white':  attr.append('37')

    if backColor == 'black':    pass
    elif backColor == 'red':    attr.append('41')
    elif backColor == 'green':  attr.append('42')
    elif backColor == 'yellow': attr.append('43')
    elif backColor == 'blue':   attr.append('44')
    elif backColor == 'magenta':    attr.append('45')
    elif backColor == 'cyan':   attr.append('46')
    elif backColor == 'white':  attr.append('47')

    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

# Clear the current text line
def clearLine():
    print('{:s}'.format(' ' * DISPLAY_MAXWIDTH), end='\r')

# Show a title string
def showTitle(title, width=DISPLAY_MAXWIDTH, line='=', color='white+'):
    print()
    if title == '':
        title = width * line
    else:
        title = '{:s}[ {:s} ]'.format(3 * line, title).ljust(width,line)

    print(colorStr(title, color))

# Show a data string
def showData(title, data):
    print('{0}{1}'.format(title.ljust(DISPLAY_DATA_TITLE_PADDING), data))

# Show a percentage string
def showPct(title, current, total):
    pct = (100 * (current / total))
    pctStr = '{:s}[{:4d}/{:4d}] ({:6.2f}%)'.format(
        title.ljust(DISPLAY_DATA_TITLE_PADDING),
        current, total, pct)

    print(colorStr(pctStr, 'cyan'), end='\r')
    sys.stdout.flush()

# Show 'normal' message
def showMsg(msg):
    print(colorStr('- ' + msg, 'yellow'))

# Show 'OK' message
def showOKMsg(msg):
    print(colorStr('[OK] ' + msg, 'green'))

# Show Received data message
def showReceivedMsg(msg):
    print(colorStr('<<< ' + msg.replace('\n',''), 'white+'))

# Show Sent data message
def showSentMsg(msg):
    print(colorStr('>>> ------------------------------------| ' + msg.replace('\n','') + ' ', 'cyan'))

# Show 'ERROR' message
def showErrorMsg(msg):
    print(colorStr('[ERROR] ' + msg, 'red+'))

# Sleep in millis
def delay(millis):
    # showMsg('Waiting ({0})'.format(millis))
    time.sleep(millis/1000)

# Abort program execution and show an error message
def abort(msg):
    print()
    showErrorMsg(msg)
    sys.exit()

# ---[ Main code section ]-----------------------------------------------------------------------------------

if __name__ == "__main__":
    print('This module is a library, it should not be executed directly')
