import requests
import pdb
class TexasApi:
    ROOT_URL = "https://data.texas.gov/resource/naix-2893.json"
    
    def __init__(self, params = {}):
        self.params = {}
        
    def find_by_id(self, venue_id):
        return f'{self.ROOT_URL}'
            
    def find_by_gt(self, month, year, amount, location = None):
        where_params = {'$where': f'(total_receipts>{amount})'}
        return self.find_by(month, year, location, where_params)
    
    def find_by_lt(self, month, year, amount, location = None):
        where_params = {'$where': f"(total_receipts<{amount}) AND (total_receipts>0)"}
        return self.find_by(month, year, location, where_params)
    
    def find_by(self, month, year, location, where_params):
        params = {"obligation_end_date_yyyymmdd": f"{year}-{month}-31T00:00:00.000"}
        params.update(where_params)
        if location:
            params.update({'location_city': location.upper()})
        find_by_url = self.full_url(params)
        return self.make_request(find_by_url)
        
        
    def full_url(self, params):
        params_s = self.params_to_s(params)
        return f"{self.ROOT_URL}{params_s}"
    
    def make_request(self, url):
        response = requests.get(url)
        venues = response.json()
        return venues

    def scoped(self, venues, selected_vals = ['total_receipts', 'taxpayer_number']):
        scoped_venues = [{k:v for k, v in venue.items() if k in selected_vals} for venue in venues]
        return scoped_venues
    
    def params_to_s(self, params):
        not_where_params = '&'.join([f"{k}={v}" for k, v in params.items() if k != '$where'])
        where_params = self.where_params(params)
        self.params_s = f"?{not_where_params}{where_params}"
        return self.params_s
    
    def where_params(self, params):
        if params.get('$where'):
            return f"&$where={params.get('$where')}" 
        else:
            return ""
        
        
        