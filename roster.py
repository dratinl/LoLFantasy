from bs4 import BeautifulSoup
import itertools
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import re
import multiprocessing as mp 
from multiprocessing import Process, current_process, Queue
from operator import itemgetter
# Webscraper file to lift Full Rosters from the gamepedia pages
def get_roster(page):
	driver = webdriver.Chrome()
	chrome_options = Options()  
	chrome_options.add_argument("--headless")  
	try: # Obtain data from gamepedia page, exiting with error if page is unreachable
		driver.set_page_load_timeout(60)
		driver.get(page)
		driver.refresh()
		SCROLL_PAUSE_TIME = 0.1
		SCROLL_LENGTH = 1500
		page_height = int(driver.execute_script("return document.body.scrollHeight"))
		scrollPosition = 0
		while scrollPosition < page_height:
			scrollPosition += SCROLL_LENGTH
			driver.execute_script("window.scrollTo(0, " + str(scrollPosition) + ");")
			time.sleep(SCROLL_PAUSE_TIME)

		soup = BeautifulSoup(driver.page_source, "html.parser")
		driver.quit()

	except TimeoutException as e:
		print("Page load Timeout Occured. Quiting !!!")
		driver.quit()

	temp = soup.select('.wikitable')
	#suh = soup.find_all('tr')
	#print(len(suh))
	#for a in suh:
	#	print(a.get_text())
	suh = temp[0].find_all('tr')
	roster =[]
	teamname = page.split(".com/")
	roster.append(teamname[1].replace('_', ''))
	for x in range(1, len(suh)):
		player = suh[x].get_text().split()
		player.pop() # Removes Contracts Details
		player.pop() # Removes Join Date
		player.pop(0) # Removes Player REgion

		player = ' '.join(player)
		player = player.replace(' Laner', '')
		player = player.split()
		role = player[len(player)-1][1:len(player[len(player)-1])]
		if 'Sub/' in role:
			role = 'Coach'
		
		roster.append(player[0] + ' ' + role)
	return roster
	
rosters = []
lcs_teams = ['https://lol.gamepedia.com/100_Thieves', 'https://lol.gamepedia.com/Cloud9', 'https://lol.gamepedia.com/Clutch_Gaming', 'https://lol.gamepedia.com/Counter_Logic_Gaming', 'https://lol.gamepedia.com/Echo_Fox', 'https://lol.gamepedia.com/FlyQuest', 'https://lol.gamepedia.com/Golden_Guardians', 'https://lol.gamepedia.com/OpTic_Gaming', 'https://lol.gamepedia.com/Team_Liquid', 'https://lol.gamepedia.com/Team_SoloMid']
for x in lcs_teams:
	rosters.append(get_roster(x))



for teams in rosters:
	count = 0
	for player in teams:
		if count < 1:
			print(f"{player} = Player('{player}', 'Team')")
			count+=1
		else:
			temp_p = player.split(' ')[0]
			temp_r = player.split(' ')[1]
			print(f"{temp_p} = Player('{temp_p}', '{temp_r}')")
			count+=1