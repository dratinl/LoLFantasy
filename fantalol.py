from bs4 import BeautifulSoup
import itertools
import requests
from lxml import etree
from selenium import webdriver
import time
import re

class Player:
	def __init__(self, name, team, position):
		self.name = name
		self.team = team
		self.position = position



def get_match(match_id):

	# Input: URL as string for League of Legends Match History
	# Output: Match Data [10[Team/Player, Kills, Deaths, Assists, CS, Gold]] + 2[Baron, Dragons, Turrets, Inhibitors]
	# Isolates relevant stats based on classes and removes unnecesarry strings

	driver = webdriver.Chrome()
	
	try :

		driver.set_page_load_timeout(120) # Following ensures pages are loaded correctly and no data is lost
		driver.get(match_id)
		SCROLL_PAUSE_TIME = 0.3
		SCROLL_LENGTH = 200
		page_height = int(driver.execute_script("return document.body.scrollHeight"))
		scrollPosition = 0

		while scrollPosition < page_height:
			scrollPosition += SCROLL_LENGTH
			driver.execute_script("window.scrollTo(0, " + str(scrollPosition) + ");")
			time.sleep(SCROLL_PAUSE_TIME)

		soup = BeautifulSoup(driver.page_source, "lxml")
		driver.quit()

	except TimeoutException as e:

		print("Page load Timeout Occured. Quiting !!!")
		driver.quit()
	
	player_r =[a for a in (x.select('.binding')for x in soup.select('.classic.player')) if a]
	results = []
	for a in player_r:
		for b in a:
			if 'item-icon' not in b.attrs['class'] and 'spell-icon' not in b.attrs['class'] and 'champion-icon' not in b.attrs['class']:
				results.append(b.get_text())

	p_results = [results[i:i+7] for i in range(0, len(results), 7)]
	for a in p_results:
		a.pop(0)


	team_r = soup.select('.classic.team-footer')
	t_results = [[],[]]
	count=0
	for b in team_r:
		#for character in b.get_text():
			#if character.isdigit():
		t_results[count].append(re.findall("\d+", b.get_text()))
		count+=1


	r = []
	r.append(t_results)
	r.append(p_results)
	

	return r

def get_match_id(page):

	# Input: Lol Gamepedia Tournament URL Page
	# Output: All matchhistory pages if available 
	# Isolates match history links on page


	driver = webdriver.Chrome()
	driver.set_page_load_timeout(60)
	driver.get(page)

	soup = BeautifulSoup(driver.page_source, "html.parser")

	temp = soup.select('a[href*="matchhistory"]')
	matches = []
	for a in temp:
		matches.append(a.get('href'))

	return matches

# Generates Match History hyperlinks via gamepedia.com tourney pages
# Obtains and outputs stats from each game to 'games.txt'
lcs_season = get_match_id('https://lol.gamepedia.com/NA_LCS/2018_Season/Summer_Season')
match_stats = []
for x in range(0,5):
	match_stats.append(get_match(lcs_season[x]))
for a in match_stats:
	for b in a:
		print(len(b))
with open('games.txt', "w+") as f:
	for a in match_stats:
		for b in a:	
			for c in b:
				for d in c:
					f.write(str(d) + " ")
				f.write('\r\n')	
	f.close()