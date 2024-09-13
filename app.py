from flask import Flask, render_template
import re
from scraper import scrape

app = Flask(__name__)

def process_cases(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    cases = re.split(r"\(\|\)!!\(\|\)", data)
    cases = [case.strip() for case in cases if case.strip()]
    cases.reverse()

    return cases

def process_urls(file_path):
    with open(file_path, "r") as f:
        urls = f.readlines()
    return urls

def process_dates(file_path):
    with open(file_path, "r") as f:
        dates = f.readlines()
    return dates

def process_keywords(file_path):
    with open(file_path, "r") as f:
        currentkeywords = f.readlines()
    finalkeywords = []
    for keyword in currentkeywords:
        if "[]![]" not in keyword:
            finalkeywords.append(keyword)
    return finalkeywords


@app.route('/')
def index():
    scrape()
    cases = process_cases('txtfiles/completed.txt')
    urls = process_urls("txtfiles/completedresponses.txt")
    dates = process_dates("txtfiles/date.txt")
    keywords = process_keywords("txtfiles/keywords.txt")
    combined_data = zip(cases, urls, dates, keywords)
    
    return render_template('index.html', combined_data=combined_data)


if __name__ == '__main__':
    app.run(debug=True)
