#Written by J. Nichols
#
#Updates log
#10.6.17: Compiled versions v1.1 and v1.2 -- v1.1 had a major bug where incorrect indexing would result in incorrect output data.
#         version 1.2 uses a different mode of string processing, as found on line 53 of main.py
#
#10.12.17: Continually updating the GUI and functionality of the program. Added many functions.
#
# 4(I).  COMPLETE 11.6.17, utilizes the os.getcwd() function
# 4(I).  Pending updates: this file needs an exception capture system where, if the user does not specify a filepath for parsing usage, the program will auto-fill a text document
#                      that resides in the program's default directory (where the actual .exe file is stored)
#
# 4(II). COMPLETE 11.6.17, converts any text document to a .csv compatible document.
# 4(II). Pending updates: remove the decimal conversion process from the GUI interface and replace with a .csv conversion process
#           NOTE: this functionality does not retain any leading zeros on the numbers... I am still looking into this issue.
#
# 4(III).
# 4(III). Pending updates: clean code and make functions more viable.
#
# 4(IV). Working on using the GUI for more than mode page parsing...
#           1. SI Testing
#           2. RV?
#
#
#


import converter
import os
import subprocess
import time
from Tkinter import *
import tkFileDialog
from tkFileDialog import askopenfilename
import drive_types


refFileName = 'C:/ParserData/test.txt'
excelPath = 'C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE'
#importFileName = 'C:\\Users\\njordan\Desktop\\testmodepage.log'
#appendFileName = 'C:\\Users\\njordan\Desktop\\adamoutestpage.log'
#csvDocumentName = 'C:\\Users\\njordan\Desktop\\adamoutestpagecsv.csv'


#Initiate a window
rootWindow = Tk()
rootWindow.title("Mode Page Parser")


#Window dimensions
rootWindow.minsize(width=570, height=775)
rootWindow.maxsize(width=570, height=775)


#Text Labels
label1 = Label(rootWindow, text="Raw Mode Page")
label1.grid(row=0, column=0)
label2 = Label(rootWindow, text="Parsed File (HEX)")
label2.grid(row=1,column=0)
label3 = Label(rootWindow, text="Parsed File (csv)")
label3.grid(row=2,column=0)


#String Entries
importEntry = Entry(rootWindow,bd=2)
importEntry.grid(row=0,column=1,ipadx=100,pady=5,padx=5)
appendEntry = Entry(rootWindow,bd=2)
appendEntry.grid(row=1,column=1,ipadx=100,pady=5,padx=5)
appendEntry.insert(0,os.getcwd()+'\hextest.txt') #this will automatically set up a file to be used in the program. Other files can be specified if the user so desires
csvEntry = Entry(rootWindow,bd=2)
csvEntry.grid(row=2, column=1,ipadx=100,pady=5,padx=5)


def fileNameCheck(file1,file2): #import, append
    if file1 is '':
        return 0
    if file2 is '':
        return 0
    return 1


def printStrings(workingString):
    textWindow.insert(INSERT,workingString + '\n') #<-- need to be able to call this function from the other file so we can write strings to the GUI textbox when using the different formats and text blocks


def printFromFile(fileName):
    textWindow.delete('1.0',END)
    newFile = open(fileName,'r')
    for line in newFile:
        printStrings(line)
    newFile.close()


def fileBrowser1():
    filename = tkFileDialog.askopenfilename(parent=rootWindow,title="Browse for import file")
    if filename is '':
        return 0
    elif filename is not '':
        importEntry.delete(0, 'end')
        importEntry.insert(0,filename)


def fileBrowser2():
    filename = tkFileDialog.askopenfilename(parent=rootWindow,title="Browse for import file")
    if filename is '':
        return 0
    elif filename is not '':
        appendEntry.delete(0, 'end')
        appendEntry.insert(0,filename)


def fileBrowser3():
    filename = tkFileDialog.askopenfilename(parent=rootWindow,title="Browse for import file")
    if filename is '':
        return 0
    elif filename is not '':
        csvEntry.delete(0, 'end')
        csvEntry.insert(0,filename)


def onclick():
    csvFileBool = checkButtonVar.get()
    importFileName = importEntry.get()
    appendFileName = appendEntry.get()
    csvFileName = csvEntry.get()

    if fileNameCheck(importFileName,appendFileName) == 0:
        textWindow.delete('1.0',END)
        textWindow.insert(INSERT,'Incorrect or missing filename strings for one or more entries.')
        return 0

    mainDocument = open(importFileName,'r')
    appendDocument = open(appendFileName,'w')
    rollingString = ''
    listButtonString = listButtonInput.get()
    convertHexBool = checkButtonVar1.get()
    openDocBool = checkButtonVar2.get()

    while True:
    # clears the text window at the bottom of the program and proceeds on to processing files
        textWindow.delete('1.0', END)

        if open(importFileName, 'r'):
            for line in mainDocument:
                if '0x' in line:
                    newString = line[line.index('0x') + len('0x'):]  # finds everything in the string after the 'keyword' and writes that data to a new string
                    print newString
                    if ':' in newString:
                        newList = []
                        firstSpace = newString.index(' ')
                        asteriskChar = newString.index('*')

                        for i in range(firstSpace, len(newString), 1):  # find the first character of our block of data
                            if newString[i] is not ' ':
                                firstChar = i
                                print ('First Char: {}'.format(firstChar))
                                break
                        for i in range(asteriskChar, firstChar, -1):  # find the last character of our block of data
                            if newString[i] is not ' ':
                                lastChar = i
                                print ('Last Char: {}'.format(lastChar))
                                break
                        for i in range(firstChar, lastChar-1, 1):
                            newList.append(newString[i])

                        newString1 = ''.join(newList)
                        print('Hex Line: {}'.format(newString1))
                        # print newString1

                        appendDocument.write(newString1 + '\n')  # \n is to shift lines in document before writing new data
                        rollingString = rollingString + newString1 + ' '
                        rollingString = converter.stringContinuityCheck(rollingString)  # makes sure that the whole string is only delimited by single spaces, replaces double spaces with single spaces
                        printStrings(newString1)

            print 'Bool stream: openDocBool? ', openDocBool, 'convertHexBool? ', convertHexBool, 'convertcsv?', csvFileBool
            appendDocument.close()

        if openDocBool == 1:  # if checkButton2 is selected...
            if convertHexBool == 1:  # convert to new hex block...
                if csvFileBool == 1:  # convert to csv... "yes, yes"
                    print openDocBool, convertHexBool, csvFileBool
                    converter.rollingStringParser(appendFileName, listButtonString, rollingString)
                    if csvFileName == '':  # non-specified file name, default
                        printStrings('No specified .csv file name. Using default name.')
                        newDocName = converter.convert_to_delimited_format(appendFileName)
                        printFromFile(newDocName)
                        os.startfile(newDocName)
                    else:  # specified file name
                        converter.convert_to_delimited_format(appendFileName)
                        printFromFile(csvFileName)
                        os.startfile(csvFileName)
                    break
                else:  # only convert to hex block... "yes, no"
                    print openDocBool, convertHexBool, csvFileBool
                    converter.rollingStringParser(appendFileName, listButtonString, rollingString)
                    printFromFile(appendFileName)  # used to write to the screen
                    os.startfile(appendFileName)
                    # os.system('start {} {}'.format('excel.exe',appendDocument))
                    break
            else:
                if csvFileBool == 1:  # convert to csv... "no, yes"
                    print openDocBool, convertHexBool, csvFileBool
                    if csvFileName == '':  # non-specified file name, default
                        printStrings('No specified .csv file name. Using default name.')
                        newDocName = converter.convert_to_delimited_format(appendFileName)
                        printFromFile(newDocName)
                        os.startfile(newDocName)
                    else:  # specified file name
                        converter.convert_to_delimited_format(appendFileName)
                        printFromFile(csvFileName)
                        os.startfile(csvFileName)
                    break
                else:  # only convert to hex block
                    print openDocBool, convertHexBool, csvFileBool
                    printFromFile(appendFileName)  # used to write to the screen
                    os.startfile(appendFileName)
                    break
                    # printFromFile(appendFileName)
                    # break
        elif openDocBool == 0:  # if checkButton2 is not selected...
            if convertHexBool == 1:  # convert to new hex block...
                if csvFileBool == 1:  # convert to csv... "yes, yes"
                    print openDocBool, convertHexBool, csvFileBool
                    converter.rollingStringParser(appendFileName, listButtonString, rollingString)
                    if csvFileName == '':  # non-specified file name, default
                        printStrings('No specified .csv file name. Using default name.')
                        newDocName = converter.convert_to_delimited_format(appendFileName)
                        printFromFile(newDocName)
                    else:  # specified file name
                        converter.convert_to_delimited_format(appendFileName)
                        printFromFile(csvFileName)
                    break
                else:  # only convert to hex block... "yes, no"
                    print openDocBool, convertHexBool, csvFileBool
                    converter.rollingStringParser(appendFileName, listButtonString, rollingString)
                    printFromFile(appendFileName)  # used to write to the screen
                    break
            else:
                if csvFileBool == 1:  # convert to csv... "no, yes"
                    print openDocBool, convertHexBool, csvFileBool
                    if csvFileName == '':  # non-specified file name, default
                        printStrings('No specified .csv file name. Using default name.')
                        newDocName = converter.convert_to_delimited_format(appendFileName)
                        printFromFile(newDocName)
                    else:  # specified file name
                        converter.convert_to_delimited_format(appendFileName)
                        printFromFile(csvFileName)
                    break
                else:  # only convert to hex block
                    print openDocBool, convertHexBool, csvFileBool
                    printFromFile(appendFileName)  # used to write to the screen
                    break


#append button. when clicked the program executes the code in the onclick command
appendButton = Button(rootWindow, text="Parse", fg='black',bg='grey',command=onclick)
appendButton.grid(row=3, column=0,ipadx=20,pady=5)


#quit button. when clicked the program exits
quitButton = Button(rootWindow, text="Quit",fg='black',bg='grey',command=rootWindow.quit)
quitButton.grid(row=3, column=2,rowspan=2,ipadx=10)


#checkbox: this checkbox returns a value of 1 or 0, 1 to convert output doc to csv, 0 to remain in hex
checkButtonVar = IntVar()
checkButton = Checkbutton(rootWindow, text='Convert to csv Format?', variable=checkButtonVar)
checkButton.grid(row=4, column=1,sticky=W)


#checkbox: this checkbox is used to indicate whether the user would like to convert the hex data block to hex data headers and page listings
checkButtonVar1 = IntVar()
checkButton1 = Checkbutton(rootWindow, text='Parse Raw Hex Data?', variable=checkButtonVar1)
checkButton1.grid(row=3, column=1,sticky=W)


checkButtonVar2 = IntVar()
checkButton2 = Checkbutton(rootWindow, text='Open Parsed files?', variable=checkButtonVar2)
checkButton2.grid(row=5, column=1,sticky=W)


browseButton1 = Button(rootWindow,text="Browse for file",command=fileBrowser1)
browseButton1.grid(row=0,column=2,padx=10)


browseButton2 = Button(rootWindow,text="Browse for file",command=fileBrowser2)
browseButton2.grid(row=1,column=2,padx=10)


browseButton3 = Button(rootWindow,text="Browse for file",command=fileBrowser3)
browseButton3.grid(row=2,column=2,padx=10)


listButtonInput = StringVar(rootWindow)
listButtonInput.set(drive_types.driveListString[0]) #sets the default value for the dropdown menu to HGST
listButton = apply(OptionMenu,(rootWindow,listButtonInput)+tuple(drive_types.driveListString))
listButton.grid(row=4,column=0,pady=5)


textWindow = Text(rootWindow,height=35,width=65,pady=15,font=('Helvetica',8),bd=3)
textWindow.grid(row=6,columnspan=4,pady=30)


#If this python file is the file called, complete all processes defined in rootWindow
if __name__ == '__main__':
      rootWindow.mainloop()
