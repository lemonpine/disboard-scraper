from bs4 import BeautifulSoup
import requests

keywords = input("input keywords eg: nitro+kpop+minecraft ")
sort = input("sort by bumped recently, or member count? [1/2] ")

if sort == "1":
    disboardUrl = f"https://disboard.org/search?keyword={keywords}&sort=bumped_at"
elif sort == "2":
    disboardUrl = f"https://disboard.org/search?keyword={keywords}&sort=-member_count"

HEADERS = {'User-Agent': 'Mozilla/5.0'}

i = 1
f = open('invites.txt', 'w')

while True:
    request = requests.get(f"{disboardUrl}&page={i}", headers=HEADERS)
    soup = BeautifulSoup(request.text, 'html.parser')
    server_card = soup.findAll('div', class_="column is-one-third-desktop is-half-tablet")

    serverIds = []
    for card in server_card:
        serverID = card.find('a', class_="button button-join is-discord").get('data-id')
        serverIds.append(serverID)
        
    for url in serverIds:
        request = requests.get(f"http://disboard.org/server/join/{url}", headers=HEADERS, allow_redirects=False)
        print(request.url)
        f.write(f'{request.url}\n')

    i = i + 1
f.close()

