import bs4
import flask
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape/deals', methods=['GET'])
def scrape_data():
    url = 'https://istyle.ro/'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('div', class_='product-item')

    scraped_data = []
    for result in results:
        product_name_element = result.find('div', class_='product-item-name')
        if product_name_element:
            product_name = product_name_element.text.strip()
            img_element = result.find('img')
            product_price_element = result.find('span', class_='price')
            if img_element and product_price_element:
                image_url = img_element.get('src')
                product_price = product_price_element.text.strip()
                scraped_data.append({
                    'name': product_name,
                    'image_url': image_url,
                    'price': product_price
                })

    return jsonify(scraped_data)

@app.route('/scrape/news', methods=['GET'])
def scrape_news():
    url = 'https://zonait.ro/stiri-stiinta-tehnologie/stiri/'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    results = soup.find_all('li', class_='post-item')

    scraped_data = []
    for result in results:
        news_title_element = result.find('h2', class_='post-title')
        if news_title_element:
            news_title = news_title_element.text.strip()
            img_element = result.find('img')
            news_link_element = news_title_element.find('a')
            if img_element and news_link_element:
                image_url = img_element.get('src')
                news_link = news_link_element.get('href')
                scraped_data.append({
                    'title': news_title,
                    'image_url': image_url,
                    'link': news_link
                })

    return jsonify(scraped_data)

# Dezactivam CORS Policy
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(debug=True)
