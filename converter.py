#Written by J. Nichols
import drive_types

def stringContinuityCheck(referenceString):
    newString = referenceString.replace('  ', ' ')
    return newString

def parseString(position1, position2, referenceString):
    refList = []
    for i in range(position1, position2, 1):
        refList.append(referenceString[i])
    newString = ''.join(refList)
    print('parseString String: {}'.format(newString))
    return newString

def determineNextIterationPosition(currentPosition,referenceString):
    refList = []
    delCurrentPosition = 0
    while True:
        for i in range(currentPosition+3,currentPosition+5,1):
            refList.append(referenceString[i])
        valueString = ''.join(refList)
        try:
            movementInt = int(valueString,16)
        except ValueError:
            return 0
        if movementInt in [0,1,2,3]:
            currentPosition+=3
            delCurrentPosition +=3
            refList = []
        else:
            adjustedMovementInt = 3*movementInt+6
            if delCurrentPosition != 0:
                return adjustedMovementInt + delCurrentPosition
            else:
                return adjustedMovementInt #returns the adjust movement of the string parser.

def rollingStringParser(fileName,driveString,rollingString):
    driveTypeIndex = drive_types.driveListString.index(driveString)
    initialPageValue = drive_types.driveList[driveTypeIndex][2] #initial page value of the selected drive type
    rollingDocument = open(fileName,"w")

    if initialPageValue in rollingString:
        POS = rollingString.index(initialPageValue)
        rollingDocument.write(parseString(0,POS-1,rollingString) + '\n') #write the INITIAL string to the text file, the HEADER
    while True:
        try:
            nextCount = determineNextIterationPosition(POS,rollingString) #<- returns the adjustedMovement for the next string of chars
            if nextCount == 0:
                break
            rollingDocument.write(parseString(POS, POS + nextCount, rollingString) + '\n')
            POS = POS + nextCount  # new position = old position + adjusted movement value
        except IndexError:
            rollingDocument.close()
            break
    rollingDocument.close()

def convert_to_delimited_format(fileName, csvFileName=''): #needs to be able to work on any filetype as long as the string is consistent (delimited by 1 space)
    refDoc = open(fileName, 'r') #<-- this file is already parsed for our use
    if csvFileName == '':
        newDocName = fileName.replace('.txt','.csv')
    else:
        newDocName = csvFileName
    delimitedDoc = open(newDocName, 'w')
    for line in refDoc:
        refString = line.replace(' ',',')
        delimitedDoc.write(refString+'\n')
    refDoc.close()
    delimitedDoc.close()
    return newDocName