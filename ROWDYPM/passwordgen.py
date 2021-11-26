import hashlib
from typing import final
from django.shortcuts import render
def genPassword(capitalsBoolean, numbersBoolean, symbolsBoolean, passphrase):
    # Checkbox on app will indicate whether the password needs uppercase or not
    upperCase = capitalsBoolean
    # Checkbox on app will indicate if the password needs numbers or not
    numbers = numbersBoolean
    # Checkbox on app will indicate if the password needs symbols or not
    symbols = symbolsBoolean
    importString = passphrase
    # Use md5sum on the passphrase to turn it into 32 char alphanumeric string
    encodeString = hashlib.md5(inputString.encode('utf-8')).hexdigest()
    # Debug block
    #print("The passphrase is: " + inputString)
    #print("Encoded string: " + encodeString)
    #print("Length of encode string: " + str(len(encodeString)))

    strlen = len(encodeString)
    newstr = ""
    numberEncode = {
        "1": "c",
        "2": "r",
        "3": "f",
        "4": "s",
        "5": "g",
        "6": "p",
        "7": "i",
        "8": "a",
        "9": "k",
        "0": "v"
        }

    symbolEncode = {
        "A": "%",
        "E": "!",
        "G": "#",
        "K": "^",
        "M": "@",
        "P": "$",
        "T": "(",
        "X": "}",
        "c": ";",
        "f": "]",
        "h": "_",
        "l": "{",
        "o": "+",
        "q": "[",
        "v": "?",
        "z": ".",
        "2": "/",
        "5": "&",
        "8": ":",
        "0": "^"
        }
    #Appply a series of shifts and substitutions to randomize string
    #1. If uppercase is True search string and change every third isalpha char to Uppercase >> DONE (GJ)
    for i in range (strlen):
        if (upperCase == "True"):
            if ((i+1)%3==0):
                if(encodeString[i].isalpha()):
                    newstr += encodeString[i].upper()
                else:
                    newstr += encodeString[i]
            else:
                newstr += encodeString[i]
        else:
            newstr += encodeString[i]
    #print("Checkpoint 1. String after UpperCase Encoding: " + newstr)

    #2. If numbers do nothing. If no numbers, change every isalpha char to a letter using dictionary >> DONE (GJ)
    for i in range (strlen):
        if (numbers == "False"):
            if(newstr[i].isalpha()):
                for key in numberEncode.keys():
                    newstr = newstr.replace(key, numberEncode[key])
    #print("Checkpoint 2. String after Number Encoding: " + newstr)



    # 3. Symbols use a dictionary or targeted swap to change numbers or letters to symbols
    #    possible symbols: ~`! @#$%^&*()_-+={[}]|\:;"'<,>.?/
    #    1=! 2=@ 3=# 4=$ 5=% 6=^ 7=& 8=* 9=( 0=) a={ b=[ c=} d=] l=| y=\ e=:
    #    We don't want to swap everything but we do want to  a decent sized list

    for i in range (strlen):
        if (symbols == "True"):
            if(newstr[i].isalpha()):
                for key in symbolEncode.keys():
                    newstr = newstr.replace(key, symbolEncode[key])
    #print("Checkpoint 3. String after Symbol Encoding: " + newstr)
    """
    4. Slice the encoded and substituted string
        - mov   e the first 4 chars to the back
        - shift every 3rd char over 2 places
        - split the string in thirds or fourths and jumble it around
    Note: while we may be able to undo all the shifts and get back the encoded passphrase
            the md5sum of the string, we will never ever get back to the passphrase. This makes it
            a secret key only the user knows. So they constantly use the same one since we never store it
    """
    # 4. Slice the encoded and substituted string
    # Note: while we may be able to undo all the shifts and get back the encoded passphrase
    #        the md5sum of the string, we will never ever get back to the passphrase. This makes it
    #        a secret key only the user knows. So they constantly use the same one since we never store it

    # Move the first four chars to the back of the string
    #print("before moving first 4: " + newstr +" "+ str(len(newstr)))
    firstFour = newstr[:4]
    updatedNewstr = newstr[4:]
    updatedNewstr = updatedNewstr + firstFour
    finalStr = ""
    #print("First four moved to back: " + updatedNewstr)

    # Shift every 3rd char over 2 places
    updatedNewstr = list(updatedNewstr)
    for i in range(len(updatedNewstr)):
        if i % 3 == 0:
            updatedNewstr[i],updatedNewstr[i+1] = updatedNewstr[i+1],updatedNewstr[i]
        else:
            continue
    for i in updatedNewstr:
        finalStr = finalStr + i
    #print("semi final str: " + finalStr)
    # Split the string into thirds and jumble the segments
    thirds = (len(finalStr) // 3)
    firstThird = finalStr[:thirds]
    secondThird = finalStr[thirds:(thirds * 2)]
    thirdThird = finalStr[(thirds * 2):]
    finalStr = thirdThird + firstThird + secondThird
    finalStr = str(finalStr)
    return finalStr