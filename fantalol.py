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

# Created by: Jacob Arriola
# E-mail: Jarriola2012@gmail.com
# Input: gamepedia tournament page
# Output: Match stats for all game

def get_match_id(page):

	# Input: Lol Gamepedia Tournament URL Page
	# Output: All matchhistory pages if available 
	# Isolates match history links on page


	driver = webdriver.Chrome()
	chrome_options = Options()  
	chrome_options.add_argument("--headless")  
	try: # Obtain data from gamepedia page, exiting with error if page is unreachable
		

		driver.set_page_load_timeout(60)
		driver.get(page)
		SCROLL_PAUSE_TIME = 0.1
		SCROLL_LENGTH = 450
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


	temp = soup.select('._toggle.mdallmatches')

	matches=[[] for x in range(0,10)]

	for z in temp:
		if "column-label-small" not in z.get('class') and "showbutton" not in str(z.get('class')):
			week = z.get('class')[2]
			week = int(re.search(r'\d+', week).group())
			_MH = "N/A"
			for b in z:
				for c in b:
					if "matchhistory" in str(c):
						_MH = c.get('href')
			matches[week-1].append(_MH)
	return matches

def get_match(match_id,x,output):
	

	# Input: URL as string for League of Legends Match History
	# Output: Match Data [10[Team+Player, Kills, Deaths, Assists, CS, Gold]] + 2[Baron, Dragons, Turrets, Inhibitors]
	# Isolates relevant stats based on classes and removes unnecesarry strings
	

	nogame = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A',['N/A', 'N/A', 'N/A', 'N/A', 'N/A'],['N/A', 'N/A', 'N/A', 'N/A', 'N/A']]
	# If match history is unavailable stats are uploaded as N/A. Can be swapped with actual stats manually
	if "matchhistory" not in match_id:
		output.put((x, nogame))
		print("Exited processing game: {} NO DATA".format(x))
	else:

		driver = webdriver.Chrome()
		chrome_options = Options()  
		chrome_options.add_argument("--headless")  
		
		try :

			driver.set_page_load_timeout(120) # Following ensures pages are loaded correctly and no data is lost
			driver.get(match_id)
			SCROLL_PAUSE_TIME = 0.3
			SCROLL_LENGTH = 200
			page_height = int(driver.execute_script("return document.body.scrollHeight"))
			scrollPosition = 0
			# Scroll to bottom of page. Driver is designed to wait until window scrolls to bottom to exit driver
			while scrollPosition < page_height:
				scrollPosition += SCROLL_LENGTH
				driver.execute_script("window.scrollTo(0, " + str(scrollPosition) + ");")
				time.sleep(SCROLL_PAUSE_TIME)

			soup = BeautifulSoup(driver.page_source, "lxml")
			driver.quit()

		except TimeoutException as e:

			print("Page load Timeout Occured. Quiting !!!")
			driver.quit()
		
		# Miscellaneous data magic to get player results and team results
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

			t_results[count].append(re.findall("\d+", b.get_text()))
			count+=1

		r = []
		
		r.append(p_results)
		r.append(t_results)
		output.put((x, r))
		#with open('games.txt', "a") as f:
		#	for a in r:
		#		for b in a:
		#			f.write(str(b)+'\r\n')
		#	f.close()
		print("Finished processing game: {}".format(x))


# Generates Match History hyperlinks via gamepedia.com tourney pages
# Obtains and outputs stats from each game to 'games.txt'

output = mp.Queue()

lcs_season = get_match_id('https://lol.gamepedia.com/NA_LCS/2018_Season/Summer_Season')
procs = []
match_stats = [[]for x in range(0,10)]
#for x in range(0, 3):
#	lcs_season[0][x] = (lcs_season[0][x], get_match(lcs_season[0][x]))
results = []
count =0

for week in lcs_season:
	recount=0
	for game in week:
		count += 1
		recount += 1
		print("Processing game: {}".format(count))
		proc = Process(target=get_match, args=(game, count, output))
		procs.append(proc)
		proc.start()
	for x in range(0,recount):
		  results.append(output.get())
	proc.join()
	
sorted_results = sorted(results, key=itemgetter(0))
for a in sorted_results:
	print(a[1])


#for x in range(0,len(lcs_season)):
#	for y in range(0,len(lcs_season[x])):
#		count+=1
#		print("Processing game: {}".format(count))
		#proc = Process(target=get_match, args=(lcs_season[x][y], count, output))
		#procs.append(proc)
		#proc.start()
	
	#for proc in procs:
	#	proc.join()
#results = [output.get() for p in procs]
#print(results)

#for x in lcs_season:	
#	for a in x:
#		if count < 5:
#			a = get_match(a)
#			count +=1

#	print(lcs_season)

# Test Case: Using 3 Samples
# Input: First 3 games of the 2018 NA LCS Summer Season
# Output: 'games.txt' updated with player/team information
#with open('games.txt', "w+") as f:
#	for week in match_stats:
#		for a in week:
#			for b in a:	
#				for c in b:
#					for d in c:
#						f.write(str(d) + " ")
#					f.write('\r\n')	
#	f.close()