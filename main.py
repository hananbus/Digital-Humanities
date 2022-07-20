import re
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def rem_empty(elem):
    if elem == "":
        return False
    return True


# takes info from specific movie and return its dict
def get_info(web_page):
    small_dict = {}
    soup = BeautifulSoup(web_page, "html.parser")
    years = soup.find(itemprop="dateCreated")
    year = years.getText()
    if (len(year) != 0) & (len(year) != 1):
        small_dict.update({"year": year})
    movie_info = soup.find_all(name="tr")
    # movie_info = driver.find_elements(By.TAG_NAME, "tr")
    for data in movie_info:
        data_td = data.find_all(name="td")
        # data_td = driver.find_elements(By.TAG_NAME, "td")
        summary = 0
        english_name = 0
        actors = 0
        director = 0
        script = 0
        production = 0
        film = 0
        editor = 0
        music = 0
        num_of_viewers = 0
        budget = 0
        for td in data_td:
            if (len(td.getText()) != 0) & (len(td.getText()) != 1):
                if summary == 1:
                    small_dict.update({"summary": td.getText().strip("\n\r\t")})
                    break
                if english_name == 1:
                    small_dict.update({"english_name": td.getText().strip("\n\r\t")})
                    break
                if actors == 1:
                    actors_text = td.getText()
                    all_a = td.find_all(name='a')
                    href = []
                    index = 0
                    for a in all_a:
                        href.insert(index, main_web + a.get('href'))
                        index += 1
                    actors_text = re.sub('[\r\t]', '', actors_text).split("\n")
                    actors_text_filter = list(filter(rem_empty, actors_text))
                    actors_final = list(map(lambda x: x.strip(), actors_text_filter))
                    actors_link_name = []
                    for i in range(len(href)):
                        actor_role = actors_final[i]
                        if ',' in actor_role:
                            actor_role = actor_role.replace(',', '(')
                            actor_role += ')'
                        actors_link_name.insert(i, {"name": actor_role, "link": href[i]})
                    small_dict.update({"actors": actors_link_name})
                    break
                if director == 1:
                    small_dict.update({"director": td.getText().strip("\n\r\t")})
                    break
                if script == 1:
                    small_dict.update({"script": td.getText().strip("\n\r\t")})
                    break
                if production == 1:
                    small_dict.update({"production": td.getText().strip("\n\r\t")})
                    break
                if film == 1:
                    small_dict.update({"film": td.getText().strip("\n\r\t")})
                    break
                if editor == 1:
                    small_dict.update({"editor": td.getText().strip("\n\r\t")})
                    break
                if music == 1:
                    small_dict.update({"music": td.getText().strip("\n\r\t")})
                    break
                if num_of_viewers == 1:
                    small_dict.update({"num_of_viewers": td.getText().strip("\n\r\t")})
                    break
                if budget == 1:
                    small_dict.update({"budget": td.getText().strip("\n\r\t")})
                    break
                if td.getText() == "תקציר":
                    summary = 1
                if td.getText() == "שם אחר/לועזי":
                    english_name = 1
                if td.getText() == "משחק":
                    actors = 1
                if td.getText() == "בימוי":
                    director = 1
                if td.getText() == "תסריט":
                    script = 1
                if td.getText() == "הפקה":
                    production = 1
                if td.getText() == "צילום":
                    film = 1
                if td.getText() == "עריכה":
                    editor = 1
                if td.getText() == "מוזיקה":
                    music = 1
                if td.getText() == "מספר צופים בישראל":
                    num_of_viewers = 1
                if td.getText() == "תקציב":
                    budget = 1
    return small_dict


main_web = "https://www.cinemaofisrael.co.il/"
URL = "https://www.cinemaofisrael.co.il/%d7%90%d7%99%d7%a0%d7%93%d7%a7%d7%a1/#"
chrome_driver_path = "C:/Users/buski/Documents/Development/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
response = requests.get(url=URL)
movie_web_page = response.text
soup = BeautifulSoup(movie_web_page, "html.parser")
movies_dict = {}
driver.get(url=URL)
sleep(3)
alphabet_tags = driver.find_element(By.CLASS_NAME, "alphabet ")
alphabet_tags = alphabet_tags.find_elements(By.TAG_NAME, "a")
sleep(2)
for letter in alphabet_tags:
    letter.click()
    sleep(2)
    movies_list = driver.find_element(By.CLASS_NAME, "listgrp")
    sleep(2)
    movies_list = movies_list.find_elements(By.TAG_NAME, "a")
    for movie in movies_list:
        sleep(2)
        movie_name = movie.text
        movie.click()
        sleep(3)
        new_URL = driver.current_url
        response = requests.get(url=new_URL)
        movie_web_page = response.text
        info = get_info(movie_web_page)
        sleep(1)
        movies_dict.update({movie_name: info})
        sleep(1)
        driver.back()
        sleep(3)
    sleep(3)
with open("movies.json", 'w', encoding='utf-8') as f:
    json.dump(movies_dict, f, ensure_ascii=False, indent=4)
driver.quit()
