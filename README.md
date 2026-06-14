# weather.api

# Weather and AQI Dashboard CLI
DESCRIPTION
A lightweight, Python-based terminal app that gives you instant weather updates and air quality health advisories for any city. It connects directly to the OpenWeatherMap API, displays formatted real-time data, and remembers your recent searches using a local file so you don't have to re-type them.

 MAIN FEATURES

# QUICK WEATHER CHECKS
Instantly see the actual temperature, what it feels like outside, humidity levels, wind speed, and an overall sky description (like "Clear Sky" or "Heavy Rain").

# AIR QUALITY AND HEALTH TIPS
Pulls live air pollution data to give you an AQI rating from 1 (Good) to 5 (Very Poor), along with clear advice on whether it's a good idea to spend time outside.

<img width="701" height="305" alt="image" src="https://github.com/user-attachments/assets/1ff5987b-acd0-4c19-9953-562e74c6a6d0" />

# SMART HISTORY TRACKING 
1. Automatically shows you what you last searched for the moment you open the app.  
2. Type history at any time to pull up a neat list of your last 5 searches.

<img width="720" height="938" alt="image" src="https://github.com/user-attachments/assets/d62c5416-1a89-4add-bdf2-5c3b85256f3f" />

# ERROR PROOF CODE
 Built to handle problems gracefully. If you misspell a city, lose your internet connection, or get a bad API response, the app won't crash or show ugly errors—it just gives you a friendly heads-up.

 <img width="717" height="178" alt="image" src="https://github.com/user-attachments/assets/ec9abeda-7e8f-4b4f-9c55-af773181b244" />

 # STACK
a. main.py: The main engine running the loop, processing user commands, and handling inputs.  
b. history.json: A simple local database file created automatically to securely store and remember your last 5 city searches.  
c. .env Management: Uses environment variables to securely lock away your private API token so it never leaks onto GitHub.




