from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import requests 
from bs4 import BeautifulSoup
from time import sleep 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument('--headless') # For not opening the browser
# options.add_argument("window-size=400,800") -> Optional when the browser will be opened

# Base URL
BASE_URL = "https://cidades.ibge.gov.br/brasil/{}/panorama"

# Cities to extract information about
cities = ['sp/campinas', 'sp/santo-andre', 'mg/montes-claros', 'mg/uberaba', 'rj/rio-de-janeiro']

# Instantiating a web driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


cities_infos = {}

# Looping through all cities
for city in cities:

    cities_infos[city] = {}
    # Loading the page
    driver.get(BASE_URL.format(city))

    # Safe sleep time for the page to load entirely, since we don't have
    # to perform a lot of requests
    sleep(4) 

    # Parsing the page URL
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # First, we find the table with the desired informations
    data = soup.find('table', attrs={'class': 'lista'})

    # Find all indicators
    infos = data.find_all('tr', attrs={'class': 'lista__indicador'})

    # Looping through all infos
    for info in infos:
        # The name of the info
        name = info.find('td', attrs={'class': 'lista__nome'}).text.strip()
        name = name.split('\n')[0]
        # td with values and units
        value_list = info.find('td', attrs={'class': 'lista__valor'})
        value = value_list.find('span').text.strip() # Gets the value
        units = value_list.find('span', attrs={'class': 'unidade'}) # Gets the units

        # Not every information has units
        if units:
            units = units.text.strip()
            if units:
                name = name + f' ({units})'

        # Adding the name to the dict
        cities_infos[city][name] = value
        

    # Printing if everything went OK
    print(f'{city} OK!')

# Writing the informations to a file      
with open('cities_infos.txt', 'w') as f:
    f.write(str(cities_infos))