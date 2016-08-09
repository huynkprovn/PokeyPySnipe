
This snipe tool will allow you to capture rare pokemon from across the world without being soft banned. It works by teleporting to the location of the pokemon, engaging it, teleporting back to your starting position, and then capturing it. This does NOT trigger a soft ban.

Instructions:

- Install python 2.7.12 from here: https://www.python.org/downloads/

- After install, copy requirements.txt to c:\python27\scripts, open command prompt and type pip install -r requirements.txt

>If you get an error 'failed to build xxhash' while installing requirements.txt, please install this file and try again: http://www.microsoft.com/en-us/download/details.aspx?id=44266

- Duplicate \pogo\config.ini.sample and rename it as config.ini

- Edit \pogo\config.ini with your information:
```
[AUTH]
 type = ptc or google
 username = username
 password = password

[CONFIG]
 startLoc = Central Park NY
 minCP = 0 >minCP setting, if left at 0, will catch all Pokemon. Adjust to your preference.
```
- Edit snipe.py line 485 with the proper filename (see pogo/encrypt/ for a list of files)

- Run launch.bat

- After you get the message stating that web server is running on port 5100, navigate to http://localhost:5100

- Paste snipe coordinates (must be xxx.xxxxxx,xxx.xxxxxx format - xxx,xxxxx:xxx,xxxxxxx and other formats do not work at this time). Optionally, you can enter the name of a Pokemon to catch at this location - if left blank, the rarest Pokemon at the location will be caught automatically. If you check the 'Ignore CP' box, it will catch the Pokemon regardless of CP (Good for Pokedex filling)


Screenshots of the tool: http://imgur.com/a/TlXyx

###CREDIT TO https://github.com/rubenvereecken/pokemongo-api for providing the API for this repo###

#HUGE THANKS# ##TO ALL OF THE DEVS THAT WORKED ON THE UNKNOWN6 issue. Encrypt dll/so from http://pgoapi.com/
