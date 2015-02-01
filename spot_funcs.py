import spotify
import time

session = spotify.Session()
session.login('jessie.salas','Poiople2')
time.sleep(2)
session.process_events()
time.sleep(1)
result = session.search('Mo money mo problems',search_type=spotify.SearchType.SUGGEST).load().tracks[0]
print result
