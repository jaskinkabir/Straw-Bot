import json
settings = {
    'testing': False,
    "guilds": [
        860332677852037150
    ],
    "prefix": "!",
    "channels": {
        "860332677852037150" :  "947930049087160360",
        "1006246190729400510" : "1018977510349877318"
    }
}

token = input("Enter token: ")

settings['token']=token

with open("settings.json", "w") as f:
    json.dump(settings, f, indent=4)
