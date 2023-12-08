#!/usr/bin/env python3

import requests
import json
from config import config
from random import randrange
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


apikey = config['apiKey']
base_url = config['base_url']
_headers = {
    "Authorization": f"Token {apikey}",
    "Content-Type": "application/json"
    }
min_score = int(config['min_score']) ## we'll edit this on the day to depending on how well people did probably be like 20 points or something

def generate_random_winner_positions(participants, winner_count):
    winners = []
    choice_pool_size = len(participants)
    if winner_count >= choice_pool_size:
        print("everyone's a winner")
        return participants
    else:
        i = 1
        while i < winner_count + 1:
            rand_no = randrange(1, choice_pool_size + 1) ## for some stupid reason randrange 
                                                         ## doesn't include the number you specifiy _up to_ 
                                                         ## i.e. randrange(1,5) doesn't include '5'
            if winners.count(rand_no) < 1:
                winners.append(rand_no)
                i = i+1

    return winners


def getScoreboard():
    url = f"{base_url}api/v1/scoreboard"
    r = requests.get(url,headers=_headers, verify=False)
    return r.json()['data']

def getUsers():
    url = f"{base_url}api/v1/users"
    r = requests.get( url, headers=_headers, verify=False)
    return r.json()['data']

def main():
    participants = []
    raw_participants = ""
    # with open("example.json","r") as f: # mock response
    #    raw_participants = json.loads(f.read())

    raw_participants = getScoreboard()
    for participant in raw_participants:
        if (int(participant['score']) > min_score and int(participant['pos']) > 1):
            participants.append(participant)


    winners = generate_random_winner_positions(participants, int(config['winners']))
    
    for w in winners:
        print(f"id:[{participants[w-1]['account_id']}] - username:[{participants[w-1]['name']}] - you get a {config['prize']}")
    


if __name__ == "__main__":
    main()

