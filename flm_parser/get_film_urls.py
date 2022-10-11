from dotenv import load_dotenv
from tqdm import tqdm
import pickle

from soup import get_soup

load_dotenv()


def get_links_from_page(page_url):
    try:
        curr_soup = get_soup(page_url)
    except Exception:
        return None
    page_links = [x['href'] for x in curr_soup.find_all('a', class_='base-movie-main-info_link__YwtP1')]
    page_links = [f'https://www.kinopoisk.ru{link}' for link in page_links]
    return page_links


def get_film_links():
    """return list of links of films"""
    links = []
    with open('checked_pages.txt', 'r') as file:
        content = file.read()
        checked_pages = [str(i) for i in content.split()] if content else []

    print('Start of walking over pages')
    for page in tqdm(range(1, 75)):
        if page in checked_pages:
            continue
        curr_link = f'https://www.kinopoisk.ru/lists/movies/country--1/?ss_subscription=ANY&page={page}'
        page_links = get_links_from_page(curr_link)
        if page_links is None:
            continue
        else:
            links.extend(page_links)
            checked_pages.append(page)

    with open('checked_pages.txt', 'w') as file:
        file.write(' '.join([str(i) for i in checked_pages]))
    return links


def get_links_in_four_cycle():
    """
    Кинопоиск не дает собрать данные за один раз, какие-то страницы пропускаются
    поэтому мы проходимся по ним 4 раза
    """
    all_links = []
    for _ in range(4):
        curr_links = get_film_links()
        all_links.extend(curr_links)
    print('len', len(all_links))
    with open('../data/links.pkl', 'wb') as file_:
        pickle.dump(all_links, file_)
    return all_links


if __name__ == '__main__':
    print('Collect urls...')
    urls = get_links_in_four_cycle()
    print('Finished')
    print(len(urls))
