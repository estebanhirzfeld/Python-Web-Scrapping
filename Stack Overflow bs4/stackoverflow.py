
from bs4 import BeautifulSoup
import requests

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

url = "https://stackoverflow.com/questions/"

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

# find Questions Container
questions_container = soup.find(id="questions")

question_list = questions_container.find_all("div", class_="s-post-summary")


for question in question_list:
  question_title = question.find('h3').text
  question_description = question.find('div', class_="s-post-summary--content-excerpt")
  question_description = question_description.text.replace("\n", "").replace("\r", "").strip()
  

  print(question_title)
  print(question_description)
  print()
  