from main import YoutubePomodoro
import json

api = YoutubePomodoro()
api.getUserPrefs()
videos = api.getVideos()

with open('videos.json','w') as outfile:
	json.dump(videos,outfile)
