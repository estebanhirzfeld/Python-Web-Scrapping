import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

session = requests.Session()

login_url = 'https://github.com/login'
login_response = session.get(login_url, headers=headers)
parser_login = html.fromstring(login_response.text)

authenticity_token = parser_login.xpath('//input[@name="authenticity_token"]/@value')

###############

session_url = 'https://github.com/session'

login_data = {
    "login": "username@mail.com",
    "password": "*********",
    "commit": "Sign in",
    "authenticity_token":authenticity_token }

session.post(
    session_url,
    data=login_data,
    headers=headers
)

repositories_url = 'https://github.com/estebanhirzfeld?tab=repositories'

session_url_response = session.get(repositories_url, headers=headers)

parser_session = html.fromstring(session_url_response.text)
meta = parser_session.xpath('//meta[@name="description"]/@content')

# NO LOGIN ###############

no_login_data = requests.get(repositories_url, headers=headers)
no_login_data_parser = html.fromstring(no_login_data.text)
no_login_meta = no_login_data_parser.xpath('//meta[@name="description"]/@content')

print(meta)
print(no_login_meta)