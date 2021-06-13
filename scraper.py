import requests


from bs4                               import BeautifulSoup
from selenium                          import webdriver
from selenium.webdriver.support.ui     import WebDriverWait
from selenium.webdriver.support        import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

keywords = input("input keywords eg: nitro+kpop+minecraft ")
sort = input("sort by bumped recently, or member count? [1/2] ")

if sort == "1":
    disboardUrl = f"https://disboard.org/search?keyword={keywords}&sort=bumped_at"
elif sort == "2":
    disboardUrl = f"https://disboard.org/search?keyword={keywords}&sort=-member_count"

i = 1
while True:
    request = requests.get(f"{disboardUrl}&page={i}", headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.text, 'html.parser')
    server_card = soup.findAll('div', class_="column is-one-third-desktop is-half-tablet")

    disboardServerIDs = []
    for card in server_card:
        disboardServerID = card.find('a', class_="button button-join is-discord").get('data-id')
        disboardServerIDs.append(disboardServerID)
        
    options = Options()
    options.add_argument('--headless') 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    
    browser = webdriver.Chrome(chrome_options=options)
    for Id in disboardServerIDs:
        browser.get(f"https://disboard.org/server/join/{Id}")
        url = WebDriverWait(browser, 10).until(EC.url_contains('https://discord.com/invite/'))
        print(browser.current_url)
        
        with open("invites.txt", "a") as file:
            file.write(f'{browser.current_url}\n')
        
    browser.close()
    i = i + 1
    

