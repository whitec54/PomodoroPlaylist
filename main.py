import config
import requests
import isodate
import math


class YoutubePomodoro:
	def __init__(self):
		self.secret = config.SECRET
		self.api_base = "https://www.googleapis.com/youtube/v3/"
		self.embed_base = "https://www.youtube.com/embed/"
		self.watch_base = "https://www.youtube.com/watch?v="

	def fetchUserPrefs(self):
		music_options = ['lofi','classical','edm']
		duration_options = [5,10,15,20,25,30,35,40,45,50,55,60]

		print("Choose a music option")
		for index,value in enumerate(music_options):
			print("["+str(index)+"] "+value)

		self.music_type = music_options[int(input("enter a number: "))]

		print("Choose a productive duration")
		for index,value in enumerate(duration_options):
			print("["+str(index)+"] "+str(value)+" minutes")

		self.productive_duration = duration_options[int(input("enter a number: "))]

		print("Choose a break duration")
		for index,value in enumerate(duration_options):
			print("["+str(index)+"] "+str(value)+" minutes")

		self.break_duration = duration_options[int(input("enter a number: "))]

	def setUserPrefs(self,user_args):
		self.music_type = user_args['genre']
		self.productive_duration = int(user_args['productive'])
		self.break_duration = int(user_args['break'])

	def getVideos(self):
		if not self.music_type:
			print("Needs user prefs")
			return

		productive_url = self.buildVideoQueryStr(self.music_type)
		productive_response = requests.get(productive_url)
		productive_response = productive_response.json()
		productive_videos = productive_response["items"]

		break_url = self.buildVideoQueryStr('h3h3')
		break_response = requests.get(break_url)
		break_response = break_response.json()
		break_videos = break_response["items"]

		self.processVideos(productive_videos,self.productive_duration)
		self.processVideos(break_videos,self.break_duration)

		videos = self.mergeLists(productive_videos,break_videos)

		return videos

	def processVideos(self,videos,duration):
		self.fetchVideoDuration(videos)
		self.removeTooShort(videos,duration)
		self.addDetails(videos,duration)

	def mergeLists(self,videos1,videos2):
		length1 = len(videos1)
		length2 = len(videos2)
		shorter_length = min(length1,length2)

		videos = []
		for i in range(shorter_length):
			videos.append(videos1[i])
			videos.append(videos2[i])

		return videos

	def fetchVideoDuration(self,videos):
		for video in videos:
			video_id =video["id"]["videoId"]
			details_url = self.api_base + "videos?id="+video_id+"&part=contentDetails&key="+self.secret
			details = requests.get(details_url).json()
			details = details["items"][0]["contentDetails"] #try catch

			duration_str = details["duration"]

			duration = isodate.parse_duration(duration_str)
			duration = math.floor(duration.total_seconds()/60)

			video["duration"] = duration

	def removeTooShort(self,videos,duration):
		temp = [video for video in videos if video['duration'] >= duration]
		videos = temp

	def addDetails(self,videos,duration):
		for video in videos:
			video_id = video['id']['videoId']

			embed_url = self.embed_base + video_id +"?end=" + str(duration*60)
			watch_url = self.watch_base + video_id

			video['embed_url'] = embed_url
			video['watch_url'] = watch_url
			video['end_seconds'] = duration*60

	def buildVideoQueryStr(self,user_query):
		query = self.handleSpaces(user_query)
		search_params = "&part=snippet&type=video&videoEmbeddable=true&videoSyndicated=true&videoDuration=long&key="
		url = self.api_base+"search" + "?q=" + query + search_params + self.secret + "&max-results=10&order=viewCount";
		return url

	def handleSpaces(self,user_query):
		user_query = user_query.strip()
		user_query = user_query.replace(" ","+")
		return user_query

	def createJSON(self):
		self.getUserPrefs()
		


if __name__ == "__main__":
	test = YoutubePomodoro()
	test.createJSON()
