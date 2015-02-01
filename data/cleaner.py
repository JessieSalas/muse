#This script cleans up the song data from its raw format, and creates initial structures
import subprocess
import pickle
import json
import time
import spotify

rap_raw = open("rap_raw.txt", "r")
rock_raw = open("rock_raw.txt","r")

titles = {}
artists = {}
songs = []

#iterate through rap file, accounting for its specific formatting

index = 0

#start spotify session
session = spotify.Session()
session.login('jessie.salas', 'Poiople2')
time.sleep(2)
session.process_events()
time.sleep(2)

for line in rap_raw:
    try:
        content = line.split("-")
        print content
        artist = ("".join( a for a in ((   "".join(content[0].split(".")[0:])   )[1:]) if a not in ("'",'1','0','2','3','4','5','6','7', '8', '9')))[1:]
        title = "".join( a for a in (((content[-1]).split("(")[0].split("ft.")[0])[1:])  if a != "'")
        print artist
        print title
        #look it up in semantic music database, see if you have its meaning
        lyrics_command = "curl -d 'name={0}' -d 'genre=rap' 'http://genius-api.com/api/songInfo'".format(title + artist)

        lyrics_response = subprocess.Popen(lyrics_command, shell=True, stdout=subprocess.PIPE)
        lyrics_response.wait()

        lyrics_response = json.loads("".join([i for i in lyrics_response.stdout]))
        lyrics_response = lyrics_response[0]['link']

        lyrics_command = "curl -d 'link={0}' -d 'genre=rap' 'http://genius-api.com/api/lyricsInfo'".format(lyrics_response)

        lyrics_response = subprocess.Popen(lyrics_command, shell=True, stdout=subprocess.PIPE)
        lyrics_response.wait()
        lyrics_response = json.loads("".join([i for i in lyrics_response.stdout]))

        lyrics = ""
        #get syntax

        verses = lyrics_response["lyrics"]["sections"]
        for section in verses:
            for val in section["verses"]:
                lyrics += val["content"]

        #get semantics 
        explanations = ""
        verses = lyrics_response["explanations"]
        for section in verses:
            explanations += verses[section]

        result = session.search(title , search_type=spotify.SearchType.SUGGEST).load().tracks[0]

        songs.append( (lyrics,explanations,result) )



        if artist not in artists:
            #make a list of song references
            artists[artist] = [songs[index]]
        else:
            artists[artist].append(songs[index])

        #only one instance of song, so don't have to do if/else
        titles[title] = songs[index]
        index +=1

    except:
        continue

out = open('tiles.pickle', 'wb')
out1 = open('artists.pickle', 'wb')
out2 = open('songs.pickle', 'wb')

pickle.dump(songs,out,protocol=pickle.HIGHEST_PROTOCOL )
pickle.dump(titles,out,protocol=pickle.HIGHEST_PROTOCOL )
pickle.dump(artists,out1, protocol=pickle.HIGHEST_PROTOCOL )

#iterate through rock file, accounting for its specific formatting
