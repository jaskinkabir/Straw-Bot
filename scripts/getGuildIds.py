import json

def getGuildIds(): 
    settings=json.load(open("settings.json"))
    """_summary_

    Returns:
        list: list of GuildIds
    """

    
    if settings["testing"]:
        ret: list[int]= settings["guildtest"]
        return ret
    else:
        ret: list[int] = settings["guilds"]
        return ret   