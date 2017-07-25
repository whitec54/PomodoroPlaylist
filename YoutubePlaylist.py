from flask import Flask, jsonify, render_template, request,json

app = Flask(__name__)

@app.route('/_supply_videos')
def supply_videos():
	with open('videos.json') as infile:    
		videos = json.load(infile)
		return jsonify(videos)

@app.route('/')
def index():
	url = "https://www.youtube.com/embed/nLEOwgm7OUQ?end=1800"	

	return render_template('index.html', url=url)

if __name__ == "__main__":
	app.run(debug=True)