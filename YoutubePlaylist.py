from flask import Flask, jsonify, render_template, request,json
from main import YoutubePomodoro

app = Flask(__name__)

@app.route('/_supply_videos', methods=['GET','POST'])
def supply_videos():
	yt = YoutubePomodoro()
	yt.setUserPrefs(request.args)
	videos = yt.getVideos()

	for video in videos:
		print(video['snippet']['title'])



	return jsonify(videos)

@app.route('/')
def index():
	url = "https://www.youtube.com/embed/nLEOwgm7OUQ?end=1800"	

	return render_template('index.html', url=url)


if __name__ == "__main__":
	app.run(debug=True)