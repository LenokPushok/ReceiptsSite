import { getToken } from "./api.js";

document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const recipeId = params.get("recipe_id");
  const token = localStorage.getItem("token");

  const navLink = document.getElementById("nav-link");
  if (token) {
    navLink.textContent = "Профиль";
    navLink.href = "profile.html";
  } else {
    navLink.textContent = "Вход";
    navLink.href = "login.html";
  }

  const mainNav = document.getElementById("main-nav");
  const roleName = localStorage.getItem("role_name");

  if (roleName === "Admin") {
    const moderationLink = document.createElement("a");
    moderationLink.href = "moderation.html";
    moderationLink.textContent = "Модерация отзывов";
    mainNav.insertBefore(moderationLink, mainNav.firstChild);
  }

  const BASE_URL = "http://localhost:8080";
  const poster = document.getElementById("recipe-poster");
  const titleEl = document.getElementById("recipe-title");
  const descEl = document.getElementById("recipe-description");
  const imdbRatingEl = document.getElementById("imdb-rating");
  const rateReelRatingEl = document.getElementById("ratereel-rating");
  const reviewsContainer = document.getElementById("reviews-container");
  const reviewFormContainer = document.getElementById("review-form-container");
  const reviewMessage = document.getElementById("review-message");

  // Показать форму если токен есть
  if (token) {
    reviewFormContainer.style.display = "block";
  }

  try {
    const recipeRes = await fetch(`${BASE_URL}/api/recipe/${recipeId}`);
    if (!recipeRes.ok) throw new Error("Ошибка загрузки данных фильма");
    const recipe = await recipeRes.json();

    poster.src = `${BASE_URL}${recipe.logo_file_url}`;
    titleEl.textContent = recipe.title;
    descEl.textContent = recipe.description;
    imdbRatingEl.textContent = recipe.imdb_rating.toFixed(1);
    rateReelRatingEl.textContent = recipe.ratereel_rating.toFixed(1);
  } catch (error) {
    console.error(error);
    descEl.textContent = "Не удалось загрузить данные о фильме.";
  }

  async function loadReviews() {
    try {
      const reviewsRes = await fetch(
        `${BASE_URL}/api/recipe/${recipeId}/review/`,
      );
      if (!reviewsRes.ok) throw new Error("Ошибка загрузки отзывов");
      const reviews = await reviewsRes.json();
      reviewsContainer.innerHTML = "";

      reviews.forEach((review) => {
        const item = document.createElement("div");
        item.className = "review-item";

        const header = document.createElement("div");
        header.className = "review-item-header";

        const star = document.createElement("span");
        star.className = "star";
        star.textContent = "★";

        const ratingVal = document.createElement("span");
        ratingVal.textContent = review.rating.toFixed(1);

        const username = document.createElement("span");
        username.textContent = review.username;

        header.appendChild(username);
        header.appendChild(star);
        header.appendChild(ratingVal);

        const content = document.createElement("div");
        content.textContent = review.content;

        item.appendChild(header);
        item.appendChild(content);

        reviewsContainer.appendChild(item);
      });
    } catch (error) {
      console.error(error);
      reviewsContainer.textContent = "Не удалось загрузить отзывы.";
    }
  }

  await loadReviews();

  const reviewRatingInput = document.getElementById("review-rating-number");
  const reviewContent = document.getElementById("review-content");
  const submitReviewBtn = document.getElementById("submit-review");

  function showReviewMessage(msg, isError = false) {
    reviewMessage.style.display = "block";
    reviewMessage.textContent = msg;
    reviewMessage.style.color = isError ? "#FF5555" : "#FFFFFF";
  }

  function clearReviewMessage() {
    reviewMessage.style.display = "none";
    reviewMessage.textContent = "";
  }

  submitReviewBtn.addEventListener("click", async () => {
    clearReviewMessage();

    if (!token) {
      showReviewMessage("Для отправки отзыва необходимо авторизоваться.", true);
      return;
    }

    const contentVal = reviewContent.value.trim();
    const ratingVal = parseFloat(reviewRatingInput.value);

    if (!contentVal || isNaN(ratingVal)) {
      showReviewMessage("Введите отзыв и корректный рейтинг.", true);
      return;
    }

    if (ratingVal < 1.0 || ratingVal > 5.0) {
      showReviewMessage("Рейтинг должен быть от 1.0 до 5.0.", true);
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/api/recipe/${recipeId}/review/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          content: contentVal,
          rating: ratingVal,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        if (errorText.includes("already left review")) {
          showReviewMessage("Вы уже оставляли отзыв.", true);
        } else {
          showReviewMessage("При отправке отзыва произошла ошибка.", true);
        }
        throw new Error(errorText);
      }

      // Если успешно
      showReviewMessage("Отзыв отправлен на модерацию.");

      // Сбросить поля
      reviewContent.value = "";
      reviewRatingInput.value = "5.0";

      await loadReviews();
    } catch (error) {
      console.error("Ошибка отправки отзыва:", error);
      // Ошибка уже показана пользователю выше.
    }
  });
});
