# Consuming a particular stack exchange api

import requests
import json

response = requests.get("https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow")

print(response) # We get <Response [200]> which means OK

# print(response.json()['items'])

# API to get title and link to questions with no answers
for data in response.json()['items']:
    if data['answer_count'] == 0:
        print(data['title'])
        print(data['link'])
    else:
        print("skipped")
    print()