import json
import time
import csv

raw = open('yasp-dump-2015-12-18.json')
# output = csv.writer(open('draft-victory.csv', 'w', newline=''))
output = csv.writer(open('draft-victory.csv', 'wb'))

# players[n].hero_id
# 0-4 = radiant, 5-9 = dire
# radiant_win = true/false

processed = 0
start = time.time()
for line in raw:
	if line.startswith(',') or line.startswith('[') or line.startswith(']'):
		continue

	data = json.loads(line)

	processed += 1
	if processed % 1000 == 0:
		print("Processed: " + str(processed))

	# filtering

	# matches greater than 25 minutes
	# if float(data['duration']) > 25 * 60:
	#	continue

	if int(data['human_players']) != 10:
		continue

	heroes = [int(p['hero_id']) for p in data['players']]
	if bool(data['radiant_win']) == True:
		victory = 1
	else:
		victory = 0

	id_array = [0] * 226
	for i, hero in enumerate(heroes):
		if i < 5:
			id_array[hero-1] = 1
		else:
			id_array[hero-1 + 113] = 1

	csv_line = id_array + [victory]
	output.writerow(csv_line)



end = time.time()
print("Finished in " + str(end - start) + " seconds")

raw.close()