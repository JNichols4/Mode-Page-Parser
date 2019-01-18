#testing environment for parsing and other commands. This file is NOT included in the final compile of the program.
#

import drive_types
#WORKING.
#s1 = "07/06/17 09:11:32:244AM  TS2  >0x185ec000:  01 ae 00 10 01 00 00 10 00 00 00 01 74 9a 42 b0  *............t.B.*"
#s2 = "0x"

#print s1.index(s2), len(s2)

#newLengthIndex = s1.index(s2) + 59
#print s1[s1.index(s2)+ len(s2):]
#newString = s1[s1.index(s2)+ len(s2):]
#print newString

print drive_types.driveList[0][1]