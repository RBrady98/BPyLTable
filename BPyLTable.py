#! python3
# CLI for displaying the BPL created by Rian Brady

from bs4 import BeautifulSoup
import requests
import click
import shutil

def getTable():
    # Get data from the guardians website
    response = requests.get('https://www.theguardian.com/football/premierleague/table')
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find(class_='table__container')
    teams = table.tbody.find_all('tr')

    tableDict = {}
    for i in range(len(teams)):
        team = teams[i]
        # Get team name
        name = team.find(class_='table-column--main').a.string.replace('\n', '')
        # Get other team info
        teamInfo = (team.find_all('td'))[2:10]
        pointsList = [str(i)]
        for score in teamInfo:
            pointsList.append(score.string)

        tableDict[name] = pointsList

    # Return dictionary with team names as keys and pointsList as the values
    return tableDict


def printTeamLine(name, infoList, width, centerVal):
    teamInfo = '{:<2} {}'.format(int(infoList[0]) + 1, name)
    teamPoints = '{}  {}  {}   {}   {}  {}  {}  {} '.format(*infoList[1:])
    print('|{:<20}{:>{w}}|'.format(teamInfo, teamPoints, w=width-20).center(centerVal))



def printTableLine(width, centerVal):
    print(('+' + ('-' * width) + '+').center(centerVal))



def displayTableTop(width, column):
    # Get width of terminal so info can be printed in the center
    printTableLine(width, column)
    print('|{:^{w}}|'.format('BARCLAYS PREMIER LEAGUE', w=width).center(column))
    printTableLine(width, column)
    print('|{:<10}{:>{w}}|'.format('P  Team', 'GP  W   D   L   F   A   GD  Pts', w=width-10).center(column))
    printTableLine(width, column)


def displayTeamAtPos(table, position):
    column, rows = shutil.get_terminal_size(fallback=(80,24))
    # Display the team and team info of team in specified position 
    displayTableTop(60, column)
    # Find team from position
    for team in table:
        if table[team][0] == str(position):
            printTeamLine(team, table[team], 60, column)            
            printTableLine(60, column)
            break


@click.command()
@click.option('--position', default=-1, help='Team at position')
@click.option('--top6', is_flag=True)
def main(position, top6):
    # Load bpl table into a dictionary
    leagueTable = getTable()
    
    # If no flags passed then print the full table
    if position == -1 and top6 == False:
        displayTable()
    elif position != -1:
        displayTeamAtPos(leagueTable, position - 1)
    elif top6:
        displayTop6()


if __name__ == '__main__':
    main()
