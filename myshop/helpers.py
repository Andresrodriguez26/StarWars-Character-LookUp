import decimal
import requests 
import requests_cache 
import json 




#setup our api cache location (this is going to make a temporary database storage for our api calls)

requests_cache.install_cache('image_cache', backend='sqlite')

def get_character(name):

    url = "https://star-wars-characters.p.rapidapi.com/46DYBV/star_wars_characters"


    headers = {
        "X-RapidAPI-Key": "5ff0a59abemsh1a7801ed3d86869p10af1bjsn0d5785b8ed5a",
        "X-RapidAPI-Host": "star-wars-characters.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    name = [character.get('name') for character in data]
    # homeworld = [character.get('homeworld') for character in data]
    return name
    



class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): 
                return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)     
    

# def marvel_des(name_):
#     data = (characters.all(name=name_)["data"]["results"][0])
#     print(data)
#     description = data["description"],
#     series = data["series"]["items"],
#     image = data["thumbnail"]["path"]+'.jpg'
#     marvel_stats = {
#         'description' : description,
#         'series' : series,
#         'image' : image
#     }
#     return marvel_stats

    