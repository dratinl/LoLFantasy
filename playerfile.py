import itertools
import requests

class Player:
	
	def __init__(self, name, team, position, kills, deaths, assists, gold_earned, cs):
		self.name = name
		self.team = team
		self.position = position
		self.kills = kills
		self.deaths = deaths 
		self.assists = assists 
		self.gold_earned = gold_earned
		self.cs = cs

class Player_Team:

	def __init__(self, name, towers, inhibs, barons, dragons, rhs):
		self.name = name
		self.towers = towers
		self.inhibs = inhibs
		self.barons = barons
		self.dragons = dragons
		self.rhs = rhs

with open('games.txt', 'r') as f:
	lines = f.readlines()
	lines = [i.strip() for i in lines]
	for a in lines:
		print(a)