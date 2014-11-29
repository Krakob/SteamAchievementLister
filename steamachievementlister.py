#! python3

'''
Gets a list of achievements and slaps them into a Google tasks list.
That's the plan, at least.
'''


################################
#### Imports
################################
import os
import json
import requests
import urllib.request
import urllib.parse


################################
#### Functions
################################
clear = lambda: os.system('cls') #Creates a clear() function, which clears the console.

def exit(message="The script will now exit. Press enter to quit!"):
    input(message)
    quit()

def input_multichoice(choices, message="Enter an entry in the left column. Take note of case sensitivity.\n"):
    '''Allows the user to choose an entry in a dict; returns the key and value.'''
    longest = 0 #Declare longest key variable.
    for key, value in choices.items():
        longest = max(len(key), longest) #Determine longest key.

    print(message)
    for key, value in choices.items():
        print("%s  %s" % (key.rjust(longest+1), value)) #Print the key, value pair centered

    while True:
        try:
            choice = input("\n")
            return choice, choices[choice] #Returns user's input (the key) and the value. If the user's input is not a key,
                                           #KeyError is raised and the user has to retry due to the loop.
        except KeyError:
            print("Invalid input! Please try again.")

def load_json(filename):
    '''Input a filename which is a json, returns it as a dict.'''
    try:
        print("Attempting to load %s..." % filename)
        with open(filename) as f:
            print("Success!\n")
            return json.load(f)
    except FileNotFoundError:
        print("Something went wrong with loading %s! Does the file exist?" % filename)
        exit()
    except ValueError:
        print("Something went wrong with loading %s! The formatting of the file is probably incorrect." % filename)
        exit()

def set_appid(apps, steam_settings):
    print("Choose Steam application to work with.")
    steam_settings["appname"], steam_settings["appid"] = input_multichoice(apps)

def get_achievements(keys, request_url="http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001"):
    '''Sends a GetPlayerAchievements request to the Steam API, with the keys contained in keys.
    Keys are: appid, steamid, key, l. l is an optional language argument
    but it's necessary to get proper names and descriptions of the achievements.
    Returns and writes the json to file.'''

    if not 'appid' in keys:
        print("No appid has yet been specified! Achievements cannot be retreived.")
    else:
        print("Attempting to retreive achievement data.\nApplication name: %s\nApplication ID: %s" % (keys["appname"], keys["appid"]))
        response = requests.get(request_url, params=keys).json()
        with open("responses/%s %s.json" % (keys['appid'], keys['appname']), 'w') as f:
            json.dump(response, f, indent = 4)
        return response


################################
#### Main code
################################
if __name__ == "__main__":
    clear()
    apps = load_json("apps.json")
    steam_settings = load_json("steam.json")
    #set_appid(apps, steam_settings)
    #print(get_achievements(steam_settings))
    '''with open("test.json", 'w') as f:
        json.dump(apps, f, indent = 4)'''