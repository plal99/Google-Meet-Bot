from GoogleMeet import *

dropTempTimeTable()
createTempTimeTable()

choice = input("Do you want to modify TT for a day (press y/n): ")
while(choice.lower() == 'y'):
    Mday = input("Enter day to be changed: ")
    Mp1 = input("Enter 1st subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp2 = input("Enter 2nd subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp3 = input("Enter 3rd subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp4 = input("Enter 4th subject (0: No change, NIL: No class, sub_name: Subject): ")
    Mp5 = input("Enter 5th subject (0: No change, NIL: No class, sub_name: Subject): ")

    modifyTempTimeTable(Mday, Mp1, Mp2, Mp3, Mp4, Mp5)
    
    choice = input("Do you want to modify TT for another day (or remodify) (press y/n): ")



