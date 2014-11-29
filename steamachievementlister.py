#! python3

'''
Gets a list of achievements and slaps them into a Google tasks list.
That's the plan, at least.
'''


################################
#### Imports
################################
import requests
import json
import urllib.request
import urllib.parse


################################
#### Functions
################################
def exit(message="The script will now exit. Press enter to quit!"):
    input(message)
    quit()

def load_json(filename):
    '''Input a filename which is a json, returns it as a dict.'''
    try:
        print("Attempting to load %s..." % filename)
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        print("Something went wrong with loading %s! Does the file exist?" % filename)
        exit()
    except ValueError:
        print("Something went wrong with loading %s! The formatting of the file is probably incorrect." % filename)
        exit()

def get_achievements(keys_dic, appid, request_url="http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001"):
    '''Sends a GetPlayerAchievements request to the Steam API, with the keys contained in keys_dic.
    Keys are: appid, steamid, key, l. l is an optional language argument but it's necessary to get proper names and descriptions of the achievements.
    An optional argument, appid_overwrite, can be used to overwrite the appid contained in the keys_dic. It will overwite keys_dic["appid"] if it's not equal to 0.'''
    if not appid_overwrite == 0:
        keys_dic[appid] = appid_overwrite
    print("Attempting to retreive achievement data.\nApplication ID: %s\nAccount ID: %s" % (keys_dic["appid"], keys_dic["steamid"]))
    keys = urllib.parse.urlencode(keys_dic)
    full_url = request_url + keys
    response = urllib.request.urlopen(full_url)
    return response.read()


################################
#### Main code
################################
if __name__ == "__main__":

    '''print("Encoding info...")
    keys = urllib.parse.urlencode(info)
    print(keys)
    full_url = achievements_url + keys
    print("Full url:", full_url)

    print("Sending request to Steam API!")
    response = urllib.request.urlopen(full_url)
    results = response.read()
    print(results)''')

    settings = load_json("steam.json")
    print(settings)
    print(get_achievements(settings["steam"]))