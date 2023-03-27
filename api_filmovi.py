import os

import requests
import json
TMDB_API_KEY = os.environ["TMDB_API_KEY"]
test = "22"

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

    def uzmi_film_API(self, filmid):

        ID = int(filmid)
        url = f"https://api.themoviedb.org/3/movie/{ID}?"

        parameters = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
        }

        response = requests.request("GET", url, headers=self.headers, data=self.payload, params=parameters)
        # print(response.text)
        json_data_film = json.loads(response.text)
        # print(json_data_film)
        # print(json_data_film["original_title"])
        # print(json_data_film["poster_path"])
        # print(json_data_film["release_date"])
        # print(json_data_film["overview"])
        print("uzet pojedinačan film")
        return json_data_film
        """response.text  je  {"adult":false,
                  "backdrop_path":"/ykl4EIbQIddiBYTrq5hghgDL9Ky.jpg",
                  "belongs_to_collection":null,
                  "budget":0,
                  "genres":[{"id":12,"name":"Adventure"},
                            {"id":35,"name":"Comedy"},
                            {"id":10751,"name":"Family"}],
                  "homepage":"",
                  "id":892527,
                  "imdb_id":"tt14073780",
                  "original_language":"fr",
                  "original_title":"King",
                  "overview":"King, a trafficked lion cub, escapes from the airport and takes refuge with Inès and Alex, who then have the crazy idea of getting him back to Africa. Anything can happen when Max their kooky grandfather, decides to join the adventure.",
                  "popularity":59.498,
                  "poster_path":"/kEyi52oFS45X5sb78kAMnfrenxm.jpg",
                  "production_companies":[{"id":17041,"logo_path":null,"name":"Full House","origin_country":""}
                      ,{"id":95747,"logo_path":"/9fP0ZNfxTzm8S7KNfHrMHGYimb3.png","name":"Maneki Films","origin_country":"FR"},{
                                              "id":157700,"logo_path":null,"name":"Borsalino Productions","origin_country":""},
                                          {"id":7981,"logo_path":"/6Yv1gIAuGkHS5Vis4UjnqHhCPWV.png","name":"Pathé","origin_country":"FR"},
                                          {"id":170034,"logo_path":null,"name":"Bellini Films","origin_country":""},
                                          {"id":83,"logo_path":"/9OQ0rm55xtlgX7KcAKMUePJSrQc.png","name":"France 2 Cinéma","origin_country":"FR"},
                                          {"id":109756,"logo_path":"/sudlIoNIIrKmVWaYD2ZVo9HGogW.png","name":"Auvergne-Rhône-Alpes Cinéma","origin_country":"FR"}],
                  "production_countries":[{"iso_3166_1":"BE","name":"Belgium"},{"iso_3166_1":"FR","name":"France"}],
                  "release_date":"2022-02-16",
                  "revenue":2551835,
                  "runtime":105,
                  "spoken_languages":[{"english_name":"French","iso_639_1":"fr","name":"Français"}],
                  "status":"Released",
                  "tagline":"",
                  "title":"King",
                  "video":false,
                  "vote_average":6.6,
                  "vote_count":141}"""
        # komandom json_data_film = json.loads(response.text) se odgovor prebacuje u recnik, rpe toga je bio izgelda u
        # json fromatu i neke unosi su prijavljivali gresku, npr. False
        recnik = {'adult': False,
                  'backdrop_path': '/ykl4EIbQIddiBYTrq5hghgDL9Ky.jpg',
                  'belongs_to_collection': None,
                  'budget': 0,
                  'genres': [{'id': 12, 'name': 'Adventure'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}],
                  'homepage': '',
                  'id': 892527,
                  'imdb_id': 'tt14073780',
                  'original_language': 'fr',
                  'original_title': 'King',
                  'overview': 'King, a trafficked lion cub, escapes from the airport and takes refuge with Inès and Alex, who then have the crazy idea of getting him back to Africa. Anything can happen when Max their kooky grandfather, decides to join the adventure.',
                  'popularity': 59.498,
                  'poster_path': '/kEyi52oFS45X5sb78kAMnfrenxm.jpg',
                  'production_companies': [{'id': 17041, 'logo_path': None, 'name': 'Full House', 'origin_country': ''},
                                           {'id': 95747, 'logo_path': '/9fP0ZNfxTzm8S7KNfHrMHGYimb3.png', 'name': 'Maneki Films', 'origin_country': 'FR'},
                                           {'id': 157700, 'logo_path': None, 'name': 'Borsalino Productions', 'origin_country': ''},
                                           {'id': 7981, 'logo_path': '/6Yv1gIAuGkHS5Vis4UjnqHhCPWV.png', 'name': 'Pathé', 'origin_country': 'FR'},
                                           {'id': 170034, 'logo_path': None, 'name': 'Bellini Films', 'origin_country': ''},
                                           {'id': 83, 'logo_path': '/9OQ0rm55xtlgX7KcAKMUePJSrQc.png', 'name': 'France 2 Cinéma', 'origin_country': 'FR'},
                                           {'id': 109756, 'logo_path': '/sudlIoNIIrKmVWaYD2ZVo9HGogW.png', 'name': 'Auvergne-Rhône-Alpes Cinéma', 'origin_country': 'FR'}
                                           ],
                  'production_countries': [{'iso_3166_1': 'BE', 'name': 'Belgium'}, {'iso_3166_1': 'FR', 'name': 'France'}],
                  'release_date': '2022-02-16',
                  'revenue': 2551835,
                  'runtime': 105,
                  'spoken_languages': [{'english_name': 'French', 'iso_639_1': 'fr', 'name': 'Français'}],
                  'status': 'Released',
                  'tagline': '',
                  'title': 'King',
                  'video': False,
                  'vote_average': 6.6,
                  'vote_count': 141}



# film = TMDB_API()
# film.uzmi_film_API()
