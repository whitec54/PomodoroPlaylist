from main import YoutubePomodoro
import json

api = YoutubePomodoro()
api.getUserPrefs()
productive_videos,break_videos = api.getVideos()

with open('productive_videos.json','w') as outfile:
	json.dump(productive_videos,outfile)


with open('break_videos.json','w') as outfile:
	json.dump(break_videos,outfile)