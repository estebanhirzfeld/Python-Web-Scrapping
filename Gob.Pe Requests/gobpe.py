import json
from unittest import result
from attr import attributes 
from lxml import html
import requests

headers = {
    "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

articles = []

response = requests.get("https://www.gob.pe/busquedas", headers=headers)

response.encoding = 'UTF-8'

parser = html.fromstring(response.text)

data = parser.xpath('//script[contains(text(),"campañas")]')[0].text_content()

initial_index = data.find('{')
data = data[initial_index:]

data = json.loads(data)

data = data["data"]["attributes"]["results"]

for article in data:
    articles.append(article)

out_file = open("data.json", "w")
json.dump(articles, out_file)
out_file.close()

print('Data saved in data.json ;)')