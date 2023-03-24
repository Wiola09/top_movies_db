import os

import requests
import json
TMDB_API_KEY = os.environ["TMDB_API_KEY"]

class TMDB_API:
    def __init__(self):
        self.url = "https://api.themoviedb.org/3/search/movie?"
        self.payload = {}
        self.headers = {}
        self.parameters = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "query": "",
            "page": 1,
            "include_adult": "true",
        }

    def uzmi_API(self, film):
        self.parameters["query"] = film
        response = requests.request("GET", self.url, headers=self.headers, data=self.payload, params=self.parameters)
        json_data = json.loads(response.text)
        return json_data["results"]



