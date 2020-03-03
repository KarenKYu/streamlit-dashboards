import pandas as pd
import requests
import pdb
import datetime

def retrieve_key(file = 'keys.json'):
    df_keys = pd.read_json(file)
    key = df_keys.to_dict('records')[0]
    version = {'v': '20200301'}
    key.update(version)
    return key

def search_venue(venue, key): 
    params = build_params(venue, key)
    root_url = "https://api.foursquare.com/v2/venues/"
    response = requests.get(root_url + '/search', params)
    venue_results = response.json()['response']['venues']
    return venue_matches(venue, venue_results)[:1]

def build_venue_query(name, city, state, address, key = {}):
    params = {
    'near': f"{city}, {state}",
    'query': f"{name}", 
    'address': f"{address}",
    }
    params.update(key)
    return params

def build_params(venue, key):
    params = {
    'near': f"{venue['location_city']}, TX",
    'query': f"{venue['location_name']}", 
    'address': f"{venue['location_address']}",
    }
    params.update(key)
    return params

def venue_matches(venue, venue_results):
    matches = []
    venue_address = venue['location_address']
    for result in venue_results:
        result_location = result.get('location', {})
        result_address = result_location.get('address', '')
        if venue_address.lower() == result_address.lower():
            matches.append(result)
    return matches

def extract_id(venue):
    return venue['id']

def find_by_id(venue_id, key):
    root_url = "https://api.foursquare.com/v2/venues"
    url = f'{root_url}/{venue_id}'
    response = requests.get(url, params = key)
    json = response.json()
    return json.get('response', {}).get('venue', {})

def find_tips_by_id(venue_id, key):
    root_url = "https://api.foursquare.com/v2/venues"
    url = f'{root_url}/{venue_id}/tips'
    response = requests.get(url, params = key)
    return response.json()['response']['tips']['items']

def extract_tip(tip):
    time = datetime.datetime.fromtimestamp(tip['createdAt'])
    return {'text': tip['text'], 'created_at': str(time), 'agree': tip['agreeCount']}

def extract_tips(tips):
    return [extract_tip(tip) for tip in tips]