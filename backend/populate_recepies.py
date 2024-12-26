import requests
from parsel import Selector
import json
import time
import uuid
import os
from api.orm.session import get_session
from api.orm import models
from api.repo.file import FileRepo
from api.repo.movie import MovieRepo
from dotenv import load_dotenv

load_dotenv()

deepl_free_token = os.getenv("DEEPL_FREE_TOKEN")


headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

deepl_headers = headers | {"Authorization": f"DeepL-Auth-Key {deepl_free_token}"}

base_url = "https://imdb.com"
top_250_url = f"{base_url}/chart/top/"

top_250_req = requests.get(top_250_url, headers=headers)
top_250_page = top_250_req.text
top_250_selector = Selector(text=top_250_page)


# make all selector search
movie_cards_from_api_xpath = "//script[@id='__NEXT_DATA__']/text()"

top_250_movies_json = json.loads(
    top_250_selector.xpath(movie_cards_from_api_xpath).get()
)
movies_cards_edges = top_250_movies_json["props"]["pageProps"]["pageData"][
    "chartTitles"
]["edges"]

for n, movie_card_edge in enumerate(movies_cards_edges):
    # parsing args from json
    movie_card = movie_card_edge["node"]
    movie_id = movie_card["id"]
    movie_title = movie_card["titleText"]["text"]
    movie_img = movie_card["primaryImage"]["url"]
    movie_rating = round(float(movie_card["ratingsSummary"]["aggregateRating"]) / 2, 1)
    movie_url = f"{base_url}/title/{movie_id}"

    print(f"Processing movie {movie_title}")

    # request film page and parse film description
    movie_req = requests.get(movie_url, headers=headers)
    movie_selector = Selector(movie_req.text)
    movie_description = movie_selector.xpath(
        "//p[@data-testid]/span[@data-testid='plot-xl']/text()"
    ).get()

    # translate description
    translation_body = {
        "text": [movie_description],
        "target_lang": "RU",
        "source_lang": "EN",
    }
    translation_req = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=deepl_headers,
        json=translation_body,
    )
    movie_description_ru = translation_req.json()["translations"][0]["text"]

    # request film image and save it
    movie_img_req = requests.get(movie_img, headers=headers)
    file_id = uuid.uuid4()
    movie_img_path = f"movies_imgs/movie_{str(file_id)}.jpg"
    with open(movie_img_path, "wb") as file:
        file.write(movie_img_req.content)

    # write File and Movie to database
    with get_session() as session:
        if not FileRepo(session).get_resources(path=movie_img_path):
            file_orm = models.File(path=movie_img_path, id=file_id)
            session.add(file_orm)
        if not MovieRepo(session).get_resources(title=movie_title):
            movie_orm = models.Movie(
                title=movie_title,
                description=movie_description_ru,
                imdb_rating=movie_rating,
                logo_file_id=file_orm.id,
            )
            session.add(movie_orm)
        session.commit()
    time.sleep(5)
