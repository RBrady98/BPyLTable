#! python3
# CLI for displaying the BPL created by Rian Brady

from bs4 import BeautifulSoup
import requests

def getTable():
    # Get data from the guardians website
    response = requests.get('https://www.theguardian.com/football/premierleague/table')
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find(class_='table__container')
    teams = table.tbody.find_all('tr')

    tableDict = {}
    for team in teams:
        # Get team name
        name = team.find(class_='table-column--main').a.string.replace('\n', '')
        # Get other team info
        teamInfo = (team.find_all('td'))[2:10]
        pointsList = []
        for score in teamInfo:
            pointsList.append(score.string)

        tableDict[name] = pointsList

    # Return dictionary with team names as keys and pointsList as the values
    return tableDict

def main():

