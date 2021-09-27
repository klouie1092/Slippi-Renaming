from slippi import Game
from time import mktime
from os import listdir, rename
from unicodedata import normalize

def parseGame(fileName):
    data = Game(fileName)

    #Haven't implemented teams file renaming yet, unsure what the format would look like
    if not data.start.is_teams:
        characters = []

        #Goes through every player in the list, if a player is NoneType, then no one was playing on that port
        for player in data.start.players:
            if player is None:
                continue

            #Saves the character and tag of the player, and makes sure that the tag is in a readable form
            characterID = player.character

            #Supports the latin characters in the name select
            characterTag = normalize('NFKC', player.tag)

            #Adds the prefix if the players tag exists, otherwise does not list the tag
            if characterTag != '':
                characterTag = '_' + characterTag

            #Adds to the list of players
            characters+=[f'{characterID.name}{characterTag}']

        #Joins the players into a single string
        charString = 'vs'.join(characters)
        stageString = data.start.stage.name

        #Only necessary to avoid duplicate file names
        timeString = int(mktime(data.metadata.date.timetuple()))

        #Constructs the new file name
        #Time string comes first in order to preserve the order of the replays
        return f'{timeString}_{charString}_{stageString}.slp'
    return None


#Goes through every file in the working directory with the 'slp' file extension and renames them
for file in listdir('.'):
    if file.endswith(".slp"):
        rename(file,parseGame(file))