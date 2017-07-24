from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/_supply_urls')
def supply_urls():
	urls = ["https://www.youtube.com/embed/hdmSovWFhig?end=1800","https://www.youtube.com/embed/TGLQ5C8JYZw?end=1800"]
	return jsonify(urls)

@app.route('/')
def index():
	url = "https://www.youtube.com/embed/nLEOwgm7OUQ?end=1800"	

	return render_template('index.html', url=url)

if __name__ == "__main__":
	app.run(debug=True)