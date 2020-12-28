import json
import itertools
from collections import Counter

f = open('events.json')

data = json.load(f)

# number of events by state
states = []
for i in data:
    for j in i["event_location"]:
        try:
            states.append(j["street_address_1"]["region"])
        except:
            pass

# Occurrences by state
states_occurrences = Counter(states)
print(states_occurrences)

# Occurrences by category
categories = [i["event_category"] for i in data]
flat = list(itertools.chain.from_iterable(categories))

# number of events by category.
category_occurrences = Counter(flat)
print(category_occurrences)
