from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

load_dotenv()

def ask_gpt(prompt, apikey):
    openAIClient = OpenAI(api_key=apikey)
    completion = openAIClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer the following question to the best of your ability. Put no text before and after the answer, just provide the answer."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def scrape():
    with open("txtfiles/completedresponses.txt", "r") as file:
        completed_urls = {line.strip() for line in file.readlines()} 
    driver.get("https://www.bailii.org/ew/cases/EWHC/Costs/2024/")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    li_tags = soup.find_all('li')

    urls = []
    for li in li_tags:
        a_tag = li.find('a', href=True)
        if a_tag:
            full_url = "https://www.bailii.org" + a_tag['href']
            if full_url not in completed_urls:  
                urls.append(full_url)
    for url in urls:
        driver.get(url)
        time.sleep(5)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        response = ask_gpt("Please summarize this case. It's in HTML format, just ignore that:" + html_content, os.getenv("OPENAI_API_KEY"))
        response2 = ask_gpt("Please get 10 keywords for the following case in this format: | Keyword1 | Keyword 2| etc. Generate 5-6 keywords maximum. NO TEXT BEFORE OR AFTER, JUST THE KEYWORDS IN THAT FORMAT. Also, no new lines. It will be in html, just ignore that and focus on the text. Here's the case:" + html_content, os.getenv("OPENAI_API_KEY"))
        with open("txtfiles/keywords.txt", "a") as f:
            f.write(f"{response2} \n")
            f.write("[]![] \n")
        date_tag = soup.find('date')
        date_text = date_tag.get_text() if date_tag else "Date not found"
        with open("txtfiles/date.txt", "a") as f:
            f.write(f"{date_text} \n")
        with open("txtfiles/completedresponses.txt", "a") as file:
            file.write(url + "\n")
        with open("txtfiles/completed.txt", "a") as file:
            file.write(response + "(|)!!(|)\n")

    return

scrape()
