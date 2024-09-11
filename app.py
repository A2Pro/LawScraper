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

@app.route('/')
def index():
    cases = process_cases('txtfiles/completed.txt')
    return render_template('index.html', cases=cases)

if __name__ == '__main__':
    app.run(debug=True)
