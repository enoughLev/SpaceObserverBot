import requests
from config import NASA_API_KEY

def get_random_space_object():
    url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&count=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            obj = data[0]
            return {
                'title': obj.get('title'),
                'explanation': obj.get('explanation'),
                'url': obj.get('url')
            }
    return None
