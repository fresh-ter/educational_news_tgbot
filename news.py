import requests
from bs4 import BeautifulSoup
import json
import tgbotSettings as tS


def get_news_from_site(index=0):
	site_url = tS.site_url + tS.news_url_part + str(index) 
	headers = {
	        'User-Agent': tS.user_agent
	      }
	r = requests.get(site_url, headers = headers)
	html_text = r.text

	# html_text = ''
	# with open('test.html', 'r') as output_file:
	#   html_text =  output_file.read()

	soup = BeautifulSoup(html_text, 'lxml')
	html_news_list = soup.find_all('div', {'class': 'views-row'})

	return html_news_list


def get_one_news_data(_html_one_news):
	site_url = tS.site_url

	news_url = site_url + _html_one_news.find('div', {'class': 'views-field-title'}).h2.a.get("href")
	news_title = _html_one_news.find('div', {'class': 'views-field-title'}).h2.a.text
	news_date = _html_one_news.find('div', {'class': 'views-field-created'}).span.text
	news_smal_text_list = _html_one_news.find('span', {'class': 'views-field-body'})
	news_smal_text_list = news_smal_text_list.span.find_all('p')
	news_smal_text = ''

	for _news in news_smal_text_list:
		news_smal_text += _news.text
	
	return {
		'title': news_title,
		'date': news_date,
		'smal_text': news_smal_text,
		'url': news_url
	}


def get_data_of_latest_news(number=5, toPrint=False, toSaveToFile=False):
	l = []
	html_news_list = ''
	news = ''
	counter = 0

	for x in range(0,number):
		if x%5 == 0:
			html_news_list = get_news_from_site(x/5)
			counter = 0

		l_part = get_one_news_data(html_news_list[counter])
		l.append(l_part)
		counter += 1

	if toPrint:
		for x in l:
			print(x['title'])
			print(x['date'])
			print(x['smal_text'])
			print(x['url'])
			print()
			print()

	if toSaveToFile:
		with open('latest_news.json', "w") as file:
			json.dump(l, file)

	return l


def main():
	get_data_of_latest_news(15, toSaveToFile=True)


if __name__ == '__main__':
	main()
