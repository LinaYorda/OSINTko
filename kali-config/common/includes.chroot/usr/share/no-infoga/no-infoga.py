#Coader :Akash Black Hat
#Date   :18/01/2023
#Time   :Night 1:30
#Mood   :Fuck off
#from opencage.geocoder import OpenCageGeocode
#from phonenumbers import ( geocoder, carrier, parse )
from os import system

import platform

kOperativeSystem = platform.system()

def Main():
    print('''
\033[32m █████╗  ██████╗  ██╗  ██╗
\033[33m██╔══██╗ ██╔══██╗ ██║  ██║
\033[34m███████║ ██████╔╝ ███████║
\033[35m██╔══██║ ██╔══██╗ ██╔══██║
\033[36m██║  ██║ ██████╔╝ ██║  ██║ \033[32mV2.0
\033[31m╚═╝  ╚═╝ ╚═════╝  ╚═╝  ╚═╝ 
\033[33m88 88b 88 888888  dP"Yb   dP""b8    db        
\033[31m88 88Yb88 88__   dP   Yb dP   `"   dPYb       
\033[38m88 88 Y88 88""   Yb   dP Yb  "88  dP__Yb      
\033[34m88 88  Y8 88      YbodP   YboodP dP""""Yb
\033[35m*****\033[38m*******\033[32mPHONE NUMBERS INFORMATION \033[38m*******\033[35m********
\033[33m*\033[31mDeveloper:\033[35mAKASH BLACK HAT
\033[35m***********\033[31m************\033[33m***************\033[32m****************''')
    print('[!] Phone number example: +56 9 1122 3344')
    Number = input('[!] This is a pad tool <Enter Your Key : >:: ')

    # https://opencagedata.com/ API KEY
    KEY = '3c3d3f1a27614afd86b3f64addc1ceb3'

    ParsedNumber = parse(Number.replace(' ', ''))
    Country = geocoder.description_for_number(ParsedNumber, 'en')
    Service = carrier.name_for_number(ParsedNumber, 'en')

    PhoneInformation = OpenCageGeocode(KEY).geocode(Country)
    Geometry = PhoneInformation[8]
    Latitude = Geometry['geometry']['lat']
    Longitude = Geometry['geometry']['lng']
    State = Geometry['components']['state']

    Annotations = PhoneInformation[0]['annotations']
    Timezone = Annotations['timezone']['name']

    Components = PhoneInformation[0]['components']
    CountryCode = Components['country_code']
    Continent = Components['continent']

    Output = f'''
=============== RESULTS ===============
 * Country: {Country} [{CountryCode.upper()}] [{Continent}]
 * State: {State} [Approximate]
 * Carrier: {Service}
 * Timezone: {Timezone}
 * Latitude: {Latitude} [Approximate]
 * Longitude: {Longitude} [Approximate]
 =======================================
'''
    print(Output)
    SaveDataResponse = input('[!] Do you want to save the information in a file?[y/N]: ')

    if SaveDataResponse.upper() == 'Y':
        LogFile = open('Log.txt', 'a')
        LogFile.write(
    f'''\
Information related to the number: {Number}
{Output}\n''')
        print('\nInformation saved in [Log.txt]')
        LogFile.close()
    else:
        print('\n:: Good buy, drink water!')

def ClearScreen() -> None:
    system('cls' if kOperativeSystem == 'Windows' else 'clear')

if __name__ == '__main__':
    try:
        ClearScreen()
        Main()
    except KeyboardInterrupt:
        print('\n:: Remember drink water!')
    except Exception:
        print('\n:: An error occurred when trying to continue with the execution of the program, it is an unhandled exception was thrown.')
 # Happy hacking
