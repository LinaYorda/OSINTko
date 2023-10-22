#!/usr/bin/env python3 

"""
GITHUB : De-Technocrats
"""

# version
VERSION = '1.0'

# import the modules
import phonenumbers, argparse, time, requests
from phonenumbers import carrier, geocoder, timezone
from json import loads
from packaging import version

# argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--isp', help='get the isp')
parser.add_argument('-l', '--location', help='get the location')
parser.add_argument('-t', '--time', help='get the time zone')
parser.add_argument('--update', action='store_true', help='check update')
args = parser.parse_args()

# class findigo
class Findigo:

    # auto run the banner
    def __init__(self) -> None:
        print("""
  _____.__            .___.__               
_/ ____\__| ____    __| _/|__| ____   ____  
\   __\|  |/    \  / __ | |  |/ ___\ /  _ \ 
 |  |  |  |   |  \/ /_/ | |  / /_/  >  <_> )
 |__|  |__|___|  /\____ | |__\___  / \____/ 
               \/      \/   /_____/  

NOTE : Findigo is small tool to information gathering phonenumbers. We create this tool for educational purposes.
    More TOOls: https://github.com/De-Technocrats
    Telegram channel: https://t.me/DeTechnocrats
    Youtube channel: https://www.youtube.com/@DeTechnocrats

           """)
        
    # this is main function
    def Main(self):

      # check if user has been choose the ISP
      if args.isp:

          # give output
          isp = carrier.name_for_number(phonenumbers.parse(args.isp), 'en')
          print(f"[+] ISP : {isp}")

      # check if user has been choose the location
      elif args.location:

          # give output
          location = geocoder.description_for_number(phonenumbers.parse(args.location), 'en')
          print(f"[+] Location : {location}")   

      # check if user has been choose the time zone
      elif args.time:

          # give output
          time_zone = timezone.time_zones_for_number(phonenumbers.parse(args.time))
          print(f"[+] Time zone : {time_zone}")

      # check if user has been choose update the tool
      elif args.update:
          # get the url
          META_URL = 'https://raw.githubusercontent.com/De-Technocrats/findigo/main/metadata.json'
          req_meta = requests.get(META_URL, timeout=5)

          # check if HTTP status code is 200 that mean success
          if req_meta.status_code == 200:
            
            # init the update
            metadata = req_meta.text
            json_data = loads(metadata)
            version_findigo = json_data['version']
    
            # check if findigo has been available new version
            if version.parse(version_findigo) > version.parse(VERSION):
    
              # if yes, give message
              print(f'[!] New update available : {version_findigo}')
    
              # ask user to update
              ask_update = input('[!] Do you want to update?[y/n]: ')
              
              # if user answer 'y' that mean yes
              if ask_update.lower() == 'y':
    
                # do update
                newVersion = requests.get("https://raw.githubusercontent.com/De-Technocrats/findigo/main/main.py")
                open("main.py", "wb").write(newVersion.content)
                print("[+] New version downloaded")
                print('[!] Findigo will be restarting in 5 seconds...')
                time.sleep(5)
                quit()
    
              # answer 'n' that mean no or else
              else:
                
                # just give pass
                pass
            
              # i think you will understand what this mean when the tool already latest version
            else:               
                print('[+] Already up to date')
 
# run 
if __name__ == '__main__':
  try:
    RUN = Findigo()
    RUN.Main()

  # handling error
  except KeyboardInterrupt:
    print('^C')
