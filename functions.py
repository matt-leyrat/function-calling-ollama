import os
import requests
import concurrent.futures
import re
import wikipedia
from bs4 import BeautifulSoup
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
    # TODO: scrape for wiki search
    try:
        search_results = wikipedia.search(query)
        return search_results
    except wikipedia.exceptions.DisambiguationError as e:
        return e.options

def random_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = response.json()
    return f"{data['setup']} {data['punchline']}"

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

def google_search(query: str) -> dict:
    """
    Shamefully borrowed from hermes-function-calling...
    Performs a Google search for the given query, retrieves the top search result URLs,
    and scrapes the text content and table data from those pages in parallel.

    Args:
        query (str): The search query.
    Returns:
        list: A list of dictionaries containing the URL, text content, and table data for each scraped page.
    """
    num_results = 2
    url = 'https://www.google.com/search'
    params = {'q': query, 'num': num_results}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.3'}
    
    # print(f"Performing google search with query: {query}\nplease wait...")
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [result.find('a')['href'] for result in soup.find_all('div', class_='tF2Cxc')]
    
    # print(f"Scraping text from urls, please wait...") 
    # [print(url) for url in urls]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(lambda url: (url, requests.get(url, headers=headers).text if isinstance(url, str) else None), url) for url in urls[:num_results] if isinstance(url, str)]
        results = []
        for future in concurrent.futures.as_completed(futures):
            url, html = future.result()
            soup = BeautifulSoup(html, 'html.parser')
            paragraphs = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]
            text_content = ' '.join(paragraphs)
            text_content = re.sub(r'\s+', ' ', text_content)
            table_data = [[cell.get_text(strip=True) for cell in row.find_all('td')] for table in soup.find_all('table') for row in table.find_all('tr')]
            if text_content or table_data:
                results.append({'url': url, 'content': text_content, 'tables': table_data})
    return results
