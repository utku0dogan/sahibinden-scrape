from flask import Flask, request
from markupsafe import escape
from scraper import scrape


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        body = request.get_json()
        return scrape(body)
    else:
        return "hello world"

