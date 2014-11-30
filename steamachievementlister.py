#! python3
'''
Gets a list of achievements and slaps them into a list importable to Google Tasks through
https://import-tasks.appspot.com/main
'''


################################
#### Imports
################################
import os
import json
import requests
import webbrowser


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
    for key, value in sorted(choices.items()):
        print("%s  %s" % (key.rjust(longest+2), value)) #Print the key, value pair centered in the console. longest+2 to create spacing between key and leftmost column.

    while True:
        try:
            choice = input("\n")
            return choice, choices[choice] #Returns user's input (the key) and the value. 
        except KeyError: #If the user's input is not a key, KeyError is raised and the user has to retry due to the infinite loop.
            print("Invalid input! Please try again.")


def input_bool(prompt="Please enter an answer. "):
    a = input(prompt+"(y/n)\n").lower()
    while True:
        if a == 'y':
            return True
        elif a == 'n':
            return False
        else:
            print('Error! Input must be "y" (yes) or "n" (no).\n')
            a = input(prompt+"(y/n)\n").lower()


def remove_unicode(string):
    '''Removes Unicode escaped sequences such as \u2122 (trademark sign), as found in lots of game names.'''
    return string.encode('ascii', 'ignore').decode()


def make_folders(*folders):
    '''Creates folders to avoid errors from get_achievements' json dumping.'''
    print("Making folders...")
    for folder_name in folders:
        if os.path.exists(folder_name):
            print("%s already exists. No action will be taken." % folder_name)
            if os.path.isfile(folder_name):
                print("Warning! %s is a file and this script may implode due to that." % folder_name)
        else:
            print("%s does not exist and will be created." % folder_name)
            os.mkdir(folder_name)
    print("\n")


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


def dump_json(dic, filename):
    '''Dumps dic to filename with proper json formatting.'''
    with open(filename, 'w') as f:
        json.dump(dic, f, indent=4)


def set_appid(apps, steam_settings):
    print("Choose Steam application to work with.")
    steam_settings["appname"], steam_settings["appid"] = input_multichoice(apps)


def get_achievements(keys, request_url="http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001"):
    '''Gets achievement info for an application, dumps info into a .json and returns it.'''
    if not 'appid' in keys:
        print("No appid has yet been specified! Achievements cannot be retreived.")
        return None
    else:
        print("Attempting to retreive achievement data.\nApplication name: %s\nApplication ID: %s" % (keys['appname'], keys['appid']))
        response = requests.get(request_url, params=keys).json()
        dump_json(response, "responses/%s %s.json" % (keys['appid'], keys['appname'])) #Writes to "<id> <name>.json" in the responses folder.
        return response


def set_tags(steam_settings):
    tags = load_json("tags/%s %s.json" % (steam_settings['appid'], steam_settings['appname']))
    game_data = load_json("responses/%s %s.json" % (steam_settings['appid'], steam_settings['appname']))
    achievements = game_data['playerstats']['achievements']

    for achievement in achievements:                    #Go through every achievement
        for tag in tags:                                #For every achievement, go through all tags
            for field, contents in tags[tag].items():   #And for every tag, go through all of its contents
                if not contents in achievement[field]:  #Check if everything specified in the tagging is in the achievement.
                    break                               #Break the loop, triggering the else
            else:
                achievement['tag'] = tag                #Assign the tag to a new entry in the dict
                print("Assigning the tag %s to the achievement %s" % (tag, achievement['name']))
        if not 'tag' in achievement: #If no tag is assigned to achievement during the loopfest or from before.
            achievement['tag'] = "Untagged"

    game_data['playerstats']['achievements'] = achievements
    dump_json(game_data, "responses/%s %s.json" % (steam_settings['appid'], steam_settings['appname']))


def get_games(keys, request_url="http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001"):
    '''Gets a list of all games a player owns, dumps apps.json styled info and returns it.'''
    if input_bool("Warning! You are about to retreive a list of games from your Steam account. This will overwrite your current apps.json file. Continue? "):
        print("Attempting to retreive game list from Steam ID %s" % steam_settings['steamid'])
        response = requests.get(request_url, params=keys).json()
        game_list = {}
        for game in response['response']['games']: #Iterate through the list of games.
            game_list[remove_unicode(game['name'])] = game['appid'] #key = app name, value = app id
        print("Games read: %s" % response['response']['game_count'])
        dump_json(game_list, "apps.json")
        return game_list



################################
#### Main code
################################
if __name__ == "__main__":
    clear()
    print("╔════════════════════════════════════╗\n║ Running Steam Achievements lister! ║\n╚════════════════════════════════════╝\n")
    apps = load_json("apps.json")
    steam_settings = load_json("steam.json")
    make_folders("responses", "lists", "tags")

    set_appid(apps, steam_settings)
    #get_achievements(steam_settings)
    set_tags(steam_settings)