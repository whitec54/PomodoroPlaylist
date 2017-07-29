from main import YoutubePomodoro
import json

api = YoutubePomodoro()
api.fetchUserPrefs()
videos = api.getVideos()

with open('videos.json','w') as outfile:
	json.dump(videos,outfile)
