import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

data_list = []

def get_headers():
    return Headers(browser="chrome", os="win").generate()

def get_links():
    url='https://spb.hh.ru/search/vacancy?text=python+django+flask&area=1&area=2'
    res = requests.get(url, headers=get_headers()).text
  

    Soup_vacancy = BeautifulSoup(res, "lxml")
    vacancies = Soup_vacancy.find(class_="vacancy-serp-content").find_all('div', class_="serp-item")

    for vacancy in vacancies:
        salary = vacancy.find('span', class_="bloko-header-section-3")
        if salary is None:
            salary = 'зарплата не указана'
        else:
            salary = salary.text.replace('\u202f', ' ')
            data_list.append(
                {
                    'Вакансия': vacancy.find('a', class_="serp-item__title").contents[0],
                    'Компания': vacancy.find('div', class_="vacancy-serp-item__meta-info-company")
                    .contents[0].text.replace('\xa0', ' '),
                    'Город': vacancy.find('div', class_="vacancy-serp-item__info").contents[1].contents[0],
                    'ссылка': vacancy.find('a', class_="serp-item__title").attrs['href'],
                    'заработная плата': salary
                }
            )
    return data_list    
  
if __name__ == "__main__":
    data = get_links()
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=5)
