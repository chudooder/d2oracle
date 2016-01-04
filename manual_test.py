import numpy
import json
import pickle

model = pickle.load(open('model.mdl', 'rb'))

hero_list = json.load(open('heroes.json'))
hero_map = {}
for hero in hero_list['heroes']:
	hero_map[hero['localized_name'].upper()] = int(hero['id'])

radiant_heroes = []
for i in range(0, 5):
	heroname = input("Radiant hero "+str(i)+": ").upper()
	radiant_heroes.append(hero_map[heroname])

dire_heroes = []
for i in range(0, 5):
	heroname = input("Dire hero "+str(i)+": ").upper()
	dire_heroes.append(hero_map[heroname])


heroes = [0] * 224
for hero in radiant_heroes:
	heroes[hero-1] = 1

for hero in dire_heroes:
	heroes[hero-1+112] = 1

predictions = model.predict(heroes)
print(predictions)