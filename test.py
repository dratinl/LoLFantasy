from playerfile import Player
from playerfile import User
from pstats import get_match_id, get_match, get_game_stats
import os
import itertools
import requests

# All imports from roster.py
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import re
import multiprocessing as mp 
from multiprocessing import Process, current_process, Queue
from operator import itemgetter


def update_players(stats):
	imports = "os", "re"
	count = 0
	for a in stats:
		game_number = a[0]
		if game_number % 5 == 0:
			count += 1
		for b in a[1]:
			for c in b:
				if c and len(c)>2:
					try:
						
						eval(c[0].split(' ')[1]).add_one(c[1], count)
						eval(c[0].split(' ')[1]).add_two(c[2], count)
						eval(c[0].split(' ')[1]).add_three(c[4], count)
						eval(c[0].split(' ')[1]).add_four(c[4][:-1], count)
						eval(c[0].split(' ')[1]).add_five(c[5], count)
						
					except IndexError as e:
						pass

# Full 2019 LCS Roster
_100Thieves = Player('100Thieves', 'Team')
Ssumday = Player('Ssumday', 'Top')
AnDa = Player('AnDa', 'Jungler')
huhi = Player('huhi', 'Mid')
Bang = Player('Bang', 'Bot')
aphromoo = Player('aphromoo', 'Support')
Ryu = Player('Ryu', 'Coach')
Cloud9 = Player('Cloud9', 'Team')
Licorice = Player('Licorice', 'Top')
Blaber = Player('Blaber', 'Jungler')
Svenskeren = Player('Svenskeren', 'Jungler')
Goldenglue = Player('Goldenglue', 'Mid')
Nisqy = Player('Nisqy', 'Mid')
Sneaky = Player('Sneaky', 'Bot')
Zeyzal = Player('Zeyzal', 'Support')
RapidStar = Player('RapidStar', 'Coach')
ClutchGaming = Player('ClutchGaming', 'Team')
Huni = Player('Huni', 'Top')
Lira = Player('Lira', 'Jungler')
Damonte = Player('Damonte', 'Mid')
Piglet = Player('Piglet', 'Bot')
Vulcan = Player('Vulcan', 'Support')
CounterLogicGaming = Player('CounterLogicGaming', 'Team')
Darshan = Player('Darshan', 'Top')
FallenBandit = Player('FallenBandit', 'Top')
Moon = Player('Moon', 'Jungler')
Wiggily = Player('Wiggily', 'Jungler')
PowerOfEvil = Player('PowerOfEvil', 'Mid')
Stixxay = Player('Stixxay', 'Bot')
Biofrost = Player('Biofrost', 'Support')
EchoFox = Player('EchoFox', 'Team')
Solo = Player('Solo', 'Top')
Rush = Player('Rush', 'Jungler')
Fenix = Player('Fenix', 'Mid')
Apollo = Player('Apollo', 'Bot')
Hakuho = Player('Hakuho', 'Support')
FlyQuest = Player('FlyQuest', 'Team')
V1per = Player('V1per', 'Top')
Santorin = Player('Santorin', 'Jungler')
Pobelter = Player('Pobelter', 'Mid')
WildTurtle = Player('WildTurtle', 'Bot')
JayJ = Player('JayJ', 'Support')
GoldenGuardians = Player('GoldenGuardians', 'Team')
Hauntzer = Player('Hauntzer', 'Top')
Contractz = Player('Contractz', 'Jungler')
Froggen = Player('Froggen', 'Mid')
Deftly = Player('Deftly', 'Bot')
Olleh = Player('Olleh', 'Support')
OpTicGaming = Player('OpTicGaming', 'Team')
Allorim = Player('Allorim', 'Top')
Dhokla = Player('Dhokla', 'Top')
Dardoch = Player('Dardoch', 'Jungler')
Meteos = Player('Meteos', 'Jungler')
Crown = Player('Crown', 'Mid')
Arrow = Player('Arrow', 'Bot')
Asta = Player('Asta', 'Bot')
BIG = Player('BIG', 'Support')
Gate = Player('Gate', 'Support')
TeamLiquid = Player('TeamLiquid', 'Team')
Impact = Player('Impact', 'Top')
Xmithie = Player('Xmithie', 'Jungler')
Jensen = Player('Jensen', 'Mid')
Doublelift = Player('Doublelift', 'Bot')
CoreJJ = Player('CoreJJ', 'Support')
TF = Player('TF blade', 'Coach')
TeamSoloMid = Player('TeamSoloMid', 'Team')
Broken = Player('Broken blade', 'Top')
Akaadian = Player('Akaadian', 'Jungler')
Bjergsen = Player('Bjergsen', 'Mid')
Zven = Player('Zven', 'Bot')
Smoothie = Player('Smoothie', 'Support')
Lustboy = Player('Lustboy', 'Coach')



# Full Econ User Roster
team_one = User('Jacob', 'Sike')
team_two = User('Nickolishus', 'Yagami')
team_three = User('Christian', 'OnePeas')
team_four = User('tylerkungpao', 'pls gank mid')
team_five = User('Ronster', 'Class 1C')
team_six = User('TeaEye', 'I Play Sion')
		
# Test Case 1
# Users: Jcup
# User Jcup with team Fantastic Beasts would like to add player Impact to his team

Team1 = User('Jcup', 'Fantastic Beasts')

print('----------------------Beginning Test Case 1----------------------')

Team1.add_player(Impact)
Team1.replace_player(Hauntzer, Impact)
print(f'Teams: {Team1.get_user()}({Team1.get_teamname()})')
print(f'Attempting to have {Team1.get_teamname()} add Impact and replace with Hauntzer')
assert Hauntzer in Team1.roster
assert Impact not in Team1.roster
assert Impact.ffteam == None
assert Hauntzer.ffteam == Team1.get_teamname()
print('Player add successful')
print('Test 1 Cleared')

# Test Case 2
# Users: Jcup, Xchin
# User Xchin would like to add player Froggen and trade him to User Jcup for player Hauntzer

print('----------------------Beginning Test Case 2----------------------')
Team2 = User('Xchin', 'Magnanimous Seats')
print(f'Teams: {Team1.get_user()}-{Team1.get_teamname()} {Team2.get_user()}-{Team2.get_teamname()}')
print(f'Attempting to add player Froggen to {Team2.get_teamname()}')
print(f'Attempting to trade players Froggen and Haunzter')
Team2.add_player(Froggen)
Team2.trade_player(Froggen, Hauntzer, Team1)
assert Hauntzer in Team2.roster
assert Froggen in Team1.roster
assert Hauntzer.ffteam == Team2.get_teamname()
assert Froggen.ffteam == Team1.get_teamname()
print('Trade Successfull')
print('Test 2 Cleared')

# Test Case 3
# Users: Jcup
# User Jcup adds players to starting lineup and shuffles them around
print('----------------------Beginning Test Case 3----------------------')
print(f'Teams: {Team1.get_user()}-{Team1.get_teamname()}')
Team1.add_player(Contractz)
Team1.add_player(GoldenGuardians)
Team1.add_player(Impact)
Team1.add_player(Deftly)
Team1.add_player(Olleh)
print('Added players [Contractz, GoldenGuardians, Impact, Deflty, Olleh] to Fantastic Beasts')
Team1.start_player(Froggen)
print('Starting player Froggen for Team Jcup')
assert Team1.starters[0].name == 'Froggen'
Team1.start_player(Contractz)
Team1.start_player(Deftly)
print('Swapping Impact for Froggen')
Team1.starter_swap(Impact, Froggen)
print('Starting players Froggen, Olleh, GoldenGuardians')
Team1.start_player(Froggen)
Team1.start_player(Olleh)
Team1.start_player(GoldenGuardians)
print('Team1 Starting Lineup:')
Team1.get_starters()
print('Test 3 Cleared')


print('----------------------Beginning Test Case 4----------------------')
print('Updating players stats with their actual values')
s_stats = get_game_stats(get_match_id('https://lol.gamepedia.com/LCS/2019_Season/Spring_Season'))
update_players(s_stats)
assert Impact.one[0]
assert Impact.one[1]
print('Update successful')