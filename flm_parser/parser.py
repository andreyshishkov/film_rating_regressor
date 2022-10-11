import numpy as np

from dotenv import load_dotenv

from tqdm import tqdm
import csv
import os
import pickle
import time

from soup import get_soup
from get_film_urls import get_links_in_four_cycle

load_dotenv()


def get_film_descr(url: str) -> list[str, float]:
    """return description, genre and rating of film"""
    soup = get_soup(url)

    rating = soup.find('span', class_='styles_value__N2Vzt').text
    rating = np.NAN if (rating == '–') else float(rating)

    descr = soup.find('div', class_='styles_synopsisSection__nJoAj').find('p').text

    genres = soup.find('div', attrs={'data-tid': '28726596'}).find('div').find_all('a')
    genres = [genre.text for genre in genres]
    genre_str = ','.join(genres)

    return [descr, genre_str, rating]


if __name__ == '__main__':

    # collect links of films
    film_links = []
    if os.path.exists('../data/links.pkl'):
        with open('../data/links.pkl', 'rb') as file_:
            film_links = pickle.load(file_)
            print('len:', len(film_links))
    else:
        film_links = get_links_in_four_cycle()
        print('len', len(film_links))
        with open('../data/links.pkl', 'wb') as file_:
            pickle.dump(film_links, file_)

    # create list of checked films
    with open('checked_films.txt', 'r') as file:
        content = file.read()
        checked_films = content.split('\n') if content else []

    # get description of films
    films = []
    print('Start to get data')
    for film_url in tqdm(film_links):
        if film_url in checked_films:
            continue
        else:
            try:
                film = get_film_descr(film_url)
                films.append(film)
                print(len(films))
                checked_films.append(film_url)
                time.sleep(2)
            except:
                time.sleep(2)

    with open('checked_films.txt', 'w') as file_:
        print(f'amount of checked links: {len(checked_films)}')
        file_.write('\n'.join(checked_films))

    headers = ['description', 'genre', 'rating']
    with open('../data/film_ratings_1.csv', 'a', encoding='utf-8-sig', newline='') as file_:
        writer = csv.writer(file_, delimiter=';')
        writer.writerow(headers)
        writer.writerows(films)
        print('File is created')
