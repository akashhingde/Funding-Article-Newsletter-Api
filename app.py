from flask import Flask, request, jsonify
from scraper import start_parsing

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

#/getnews Api end point to fetch articles
@app.route("/getnews", methods=["GET"])
def call_news_api():
    resp = start_parsing()
    if resp["status"] == "SUCCESS":
        return jsonify(resp)
    else:
        return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
