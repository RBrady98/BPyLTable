#! python3
# CLI for displaying the BPL created by Rian Brady

from bs4 import BeautifulSoup
import requests

print('hi')

# Get data from the guardians website
response = requests.get('https://www.theguardian.com/football/premierleague/table')

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find(class_='table__container')
teams = table.tbody.find_all('tr')

for i in range(len(teams)):
    team = teams[i]
    name = team.find(class_='table-column--main').a.string.replace('\n', '')
    print(str(i) + ' ' + name)
