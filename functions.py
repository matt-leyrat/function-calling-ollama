import os
import requests
import wikipedia
from dotenv import load_dotenv
from googlesearch import search

load_dotenv()

def get_news(query, num_results=5):
    api_key = os.environ.get('NEWS_API_KEY')
    
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    articles = []
    for article in data['articles'][:num_results]:
        articles.append({
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'publishedAt': article['publishedAt']
        })
    
    return articles

def wiki_search(query):
    try:
        search_results = wikipedia.search(query)
        return search_results
    except wikipedia.exceptions.DisambiguationError as e:
        return e.options

def random_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = response.json()
    return f"{data['setup']} {data['punchline']}"

def google_search(query):
    search_results = []
    for result in search(query, num_results=5):
        search_results.append(result)
    return search_results

def get_current_weather(location, unit):
    api_key = os.environ.get("WEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "units": unit,
        "appid": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        weather_info = {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather_info
    else:
        return None
