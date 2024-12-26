import requests
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

usernames = [
    "AlexeyPetrov",
    "DmitrySokolov",
    "SergeyKuznetsov",
    "AndreyIvanov",
    "NikolaySmirnov",
    "VladimirKiselev",
    "MikhailPopov",
    "ArtemMorozov",
    "RomanVolkov",
    "EgorNikolaev",
    "KonstantinLebedev",
    "IlyaOrlov",
    "PavelVasiliev",
    "TimurFedorov",
    "YuriGavrilov",
    "KirillZaitsev",
    "OlegSemenov",
    "VictorMakarov",
    "MaximAndreev",
    "AntonAlexandrov",
]

reviews = {
    "Очень вкусное, но не для всех.": 4.7,
    "Отличный рецепт, рекомендую попробовать.": 4.6,
    "Блюдо не без недостатков, но есть можно.": 4.0,
    "Не впечатлило, слишком банально.": 4.9,
    "Понравился вкус, но подача обычная.": 4.9,
    "Очень ароматное, но текстура не идеальная.": 4.4,
    "Мне понравилось, особенно соус!": 3.8,
    "Достойный рецепт, но не шедевр.": 4.8,
    "Блюдо хорошее, но второй раз не приготовлю.": 3.4,
    "Очень понравилось сочетание ингредиентов.": 4.6,
    "Слишком сложно готовить, но результат радует.": 5.0,
    "Вкусно, но немного пересолено.": 4.6,
    "Ингредиенты отличные, но процесс долгий.": 4.8,
    "Неплохой рецепт, но повторять не буду.": 4.3,
    "Не хватило насыщенности вкуса.": 4.3,
    "Рецепт довольно хороший, но не идеальный.": 3.1,
    "Слишком долго, но в целом нормально.": 4.0,
    "Просто отличный рецепт, рекомендую всем!": 4.7,
    "Оставил много вопросов, но вкус интересный!": 4.1,
    "Ингредиенты свежие, но результат не зашёл.": 3.7,
    "Оставляет смешанные впечатления, 50/50.": 4.5,
    "Рекомендую, хотя есть свои недочёты.": 4.0,
    "Много шагов, но результат того стоит.": 3.1,
    "Было бы лучше, если бы упростили процесс.": 4.3,
    "Рецепт с интересной идеей, мне понравилось.": 3.4,
    "Много ненужных шагов, но блюдо вкусное.": 4.9,
    "Тяжеловатое блюдо, но качественное.": 3.3,
    "Лёгкий рецепт для повседневного приготовления.": 4.5,
    "Процесс сложный, но подача красивая.": 3.7,
    "Нормальный рецепт, но есть куда улучшать.": 4.7,
    "Отличное блюдо для семейного ужина.": 3.6,
    "Красиво выглядит, но вкус обычный.": 3.0
}


base_url = "http://localhost:8080"
default_password = os.getenv("DEFAULT_USER_PASSWORD")

usernames_tokens = {}

random.seed(time.time())

# fake users authentication
for username in usernames:
    auth_json = {"username": username, "password": default_password}
    print(f"Authenticating {username}")
    auth_req = requests.post(base_url + "/api/token", json=auth_json)
    if auth_req.status_code != 202:
        print(f"\tCreating user {username}")
        requests.post(base_url + "/api/user", json=auth_json)
    auth_req = requests.post(base_url + "/api/token", json=auth_json)
    if auth_req.status_code == 202:
        print(f"User {username} authenticated")
        usernames_tokens.update({username: auth_req.json()})
    print()
print()

# getting recepies
print("Getting recepies list")
recepies = requests.get(base_url + "/api/recipe").json()
print()

# making reviews
for recipe in recepies:
    recipe_title = recipe["title"]
    recipe_id = recipe["id"]
    print(f"Processing recipe {recipe_title} : {recipe_id}")
    usernames_to_leave_review = random.sample(usernames, 10)
    print(f"Users selected to leave review: {usernames_to_leave_review}")
    for username in usernames_to_leave_review:
        user_token = usernames_tokens[username]
        review_content, review_rating = random.choice(list(reviews.items()))
        print(f"Selected review {review_content} with rating {review_rating}")
        review_req = requests.post(
            base_url + f"/api/recipe/{recipe_id}/review",
            json={"content": review_content, "rating": review_rating},
            headers={"Authorization": f"Bearer {user_token}"},
        )
        if review_req.status_code == 201:
            print(f"User {username} left review for recipe {recipe_id}")
    print()
