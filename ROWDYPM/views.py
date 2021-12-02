import random
import favicon
import ssl
import hashlib
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
from .models import Password
from typing import final

# intialize key use
fernet = Fernet(settings.KEY.encode())

# initialize browser instance
ssl._create_default_https_context = ssl._create_unverified_context
browser = Browser()
browser.set_handle_robots(False)

def testfun(email, capitalsBoolean, numbersBoolean, symbolsBoolean, passphrase):
    testfunOut = "Email: {}\t booleans: {} {} {}\t passphrase: ".format(email, capitalsBoolean, numbersBoolean, symbolsBoolean, passphrase)
    print("testfun: the email is: ", testfunOut)
    password = create_password(True, True, True, "12/25/2021")
    print("testfun: 12/25/2021 -> ", password)
    return testfunOut

def listToString(stringToConvert): 
    # initialize an empty string
    returnString = "" 
    # traverse in the string  
    for ele in stringToConvert: 
        returnString += ele  
    # return string  
    return returnString 

def create_password(capitalsBoolean, numbersBoolean, symbolsBoolean, passphrase):
    # Checkbox on app will indicate whether the password needs uppercase or not
    upperCase = capitalsBoolean
    # Checkbox on app will indicate if the password needs numbers or not
    numbers = numbersBoolean
    # Checkbox on app will indicate if the password needs symbols or not
    symbols = symbolsBoolean
    inputString = passphrase
    # Use md5sum on the passphrase to turn it into 32 char alphanumeric string
    encodeString = hashlib.md5(inputString.encode('utf-8')).hexdigest()

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
    expansionList = ['g', 'h', 'i', 'j', 'k', 'n', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z']
    # Expand hexadecimal output of MD5SUM to improve complexity 
    # 17 x 2 = 34 expansion letters -> 34 + 12 via hex letters + 10nums + 20 symbols = 76**32 combinations
    encodeString = list(encodeString)
    expansionElem = 0
    for encodeElem in range(len(encodeString)):
        expansion = False
        if encodeElem % 2 == 0: 
            while expansion == False:
                encodeString[encodeElem] = expansionList[expansionElem]
                expansionElem += 1
                expansion = True
    
    encodeString = listToString(encodeString) 
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
    firstFour = newstr[:4]
    updatedNewstr = newstr[4:]
    updatedNewstr = updatedNewstr + firstFour
    finalStr = ""

    # Shift every 3rd char over 2 places
    tempChar1 = ""
    tempChar2 = ""
    updatedNewstr = list(updatedNewstr)
    for i in range(len(updatedNewstr)):
        if i % 3 == 0:
            updatedNewstr[i],updatedNewstr[i+1] = updatedNewstr[i+1],updatedNewstr[i]
        else:
            continue
    
    finalStr = listToString(updatedNewstr)
    # Split the string into thirds and jumble the segments
    thirds = (len(finalStr) // 3)
    firstThird = finalStr[:thirds]
    secondThird = finalStr[thirds:(thirds * 2)]
    thirdThird = finalStr[(thirds * 2):]
    finalStr = thirdThird + firstThird + secondThird
    finalStr = str(finalStr)
    return finalStr

def home(request):
    if request.method == "POST":
        # Sign Up
        if "register" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirmPassword = request.POST.get("confirmPassword")
            # Check password and password verification fields
            if password != confirmPassword:
                msg = "Please verify that password fields are identical."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            # Check if username is already in use
            elif User.objects.filter(username=username).exists():
                msg = f"{username} already exists"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            # Check if email is already in use
            elif User.objects.filter(email=email).exists():
                msg = f"{email} already exists"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            # Create user
            else:
                User.objects.create_user(username=username, email=email, password=password)
                newAccount = authenticate(request, username=username, password=confirmPassword, email=email)
                if newAccount is not None:
                    login(request, newAccount)
                    msg = f"Welcome {username}! Thank you for using Rowdy Password Manager."
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.path)
        # Logout
        elif "logout" in request.POST:
            msg = f"Logout successful. Thank you for using Rowdy Password Manager."
            logout(request)
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        # Login
        elif "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            loginAttempt = authenticate(request, username=username, password=password)
            if loginAttempt is None:
                msg = f"Login attempt failed. Please check username and password and try again."
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                code = str(random.randint(100000,999999))
                global globalCode
                globalCode = code
                send_mail(
                    "Rowdy Password Manager: Confirmation email",
                    f"Your verifcation code is: {code}",
                    settings.EMAIL_HOST_USER,
                    [loginAttempt.email],
                    fail_silently=False,
                )
                return render(request, "home.html", {
                        "code":code,
                        "user":loginAttempt,
                    }
                )
        # Login Confirmation
        elif "confirm" in request.POST:
            verificationCode = request.POST.get("code")
            user = request.POST.get("user")
            if verificationCode != globalCode:
                msg = f"Verfication code input {verificationCode}, does not match"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                login(request, User.objects.get(username=user))
                msg = f"Verification Successful. Welcome back {request.user}!"
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        # Store new password
        
        elif "add-password" in request.POST:
            numbersBoolean = request.POST.get("numbersBoolean", False) if True else False
            capitalsBoolean = request.POST.get("capitalsBoolean", False) if True else False
            symbolsBoolean = request.POST.get("symbolsBoolean", False) if True else False
            url = request.POST.get("url")
            email = request.POST.get("email")
            passphrase = request.POST.get("passphrase")
            password = create_password(capitalsBoolean, numbersBoolean, symbolsBoolean, passphrase)
            #encrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            
            #get title of the website
            browser.open(url)
            title = browser.title()
            #get the logo's URL
            icon = favicon.get(url)[0].url
            #Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                URL_logo=icon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )
            msg = f"{title} added successfully."
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
            
        elif "delete" in request.POST:
            urlToDelete = request.POST.get("password_id")
            msg = f"Successfully deleted: {Password.objects.get(id=urlToDelete).name}"
            Password.objects.get(id=urlToDelete).delete()
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
    
    # Display accounts instead of static cards
    accountContents = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
        accountContents = {"passwords":passwords}
    return render(request, "home.html", accountContents)