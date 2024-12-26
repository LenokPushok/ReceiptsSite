from api.routes import user, token, movie, file, movie_review, user_review, review

routers = [
    user.router,
    token.router,
    movie.router,
    file.router,
    movie_review.router,
    user_review.router,
    review.router,
]
