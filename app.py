from flask import Flask, render_template, request
import re
from dateutil import parser
from datetime import datetime

app = Flask(__name__)

def process_cases(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    cases = re.split(r"\(\|\)!!\(\|\)", data)
    cases = [case.strip() for case in cases if case.strip()]

    return cases

def process_urls(file_path):
    with open(file_path, "r") as f:
        urls = f.readlines()
    return urls

def process_dates(file_path):
    with open(file_path, "r") as f:
        dates = f.readlines()
    
    formatted_dates = []
    for date_str in dates:
        date_str = date_str.strip() 
        formatted_date = format_date(date_str)
        formatted_dates.append(formatted_date)
    for date in formatted_dates:
        if "Unknown string format" in date:
            date = date.split(":")[1]
    return formatted_dates

def format_date(date_str):
    try:
        parsed_date = parser.parse(date_str)
        formatted_date = parsed_date.strftime('%d %B %Y')
        print(formatted_date)
        
        return formatted_date
    except Exception as e:
        print(e)
        return f"Error: {e}"

def process_keywords(file_path):
    with open(file_path, "r") as f:
        currentkeywords = f.readlines()
    finalkeywords = []
    for keyword in currentkeywords:
        if "[]![]" not in keyword:
            finalkeywords.append(keyword)
    return finalkeywords

@app.route('/', methods=['GET', 'POST'])
def index():
    cases = process_cases('txtfiles/completed.txt')
    urls = process_urls("txtfiles/completedresponses.txt")
    dates = process_dates("txtfiles/date.txt")
    keywords = process_keywords("txtfiles/keywords.txt")
    
    search_query = request.form.get('search', '').lower().strip()
    
    if search_query:
        filtered_data = []
        for case, url, date, keyword in zip(cases, urls, dates, keywords):
            if (search_query in case.lower() or
                search_query in date.lower() or
                search_query in keyword.lower()):
                filtered_data.append((case, url, date, keyword))
    else:
        filtered_data = zip(cases, urls, dates, keywords)
    
    return render_template('index.html', combined_data=filtered_data, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True, port = 8080)
