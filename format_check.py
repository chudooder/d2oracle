import json
raw = open('yasp-dump-2015-12-18.json')

next(raw)
match = next(raw)

output = open('match.json', 'w')
json.dump(json.loads(match), output, indent=4)