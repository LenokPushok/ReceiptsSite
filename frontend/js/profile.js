document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("token");
  const roleName = localStorage.getItem("role_name");
  const username = localStorage.getItem("username");
  const navLink = document.getElementById("nav-link");

  if (token) {
    navLink.textContent = "Профиль";
    navLink.href = "profile.html";
  } else {
    // Если нет токена - редирект на страницу входа или главную
    window.location.href = "login.html";
    return;
  }

  // Если роль Admin, добавить ссылку "Модерация отзывов" перед "рецепты"
  const mainNav = document.getElementById("main-nav");
  if (roleName === "Admin") {
    const moderationLink = document.createElement("a");
    moderationLink.href = "moderation.html";
    moderationLink.textContent = "Модерация отзывов";
    mainNav.insertBefore(moderationLink, mainNav.firstChild);
  }

  const welcomeTitle = document.getElementById("welcome-title");
  welcomeTitle.textContent = `Привет, ${username}!`;

  const BASE_URL = "http://localhost:8080";
  const userReviewsContainer = document.getElementById("user-reviews");

  // Загрузим отзывы пользователя
  try {
    const res = await fetch(`${BASE_URL}/api/user/review/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!res.ok) throw new Error("Ошибка загрузки отзывов пользователя");
    const reviews = await res.json();

    // Если нет отзывов - можно вывести какое-то сообщение
    if (reviews.length === 0) {
      userReviewsContainer.textContent = "У вас еще нет отзывов.";
    } else {
      for (const review of reviews) {
        // Получим данные о рецепте
        const recipeRes = await fetch(
          `${BASE_URL}/api/recipe/${review.recipe_id}`,
        );
        if (!recipeRes.ok) throw new Error("Ошибка загрузки данных о рецепте");
        const recipe = await recipeRes.json();

        // Создаем карточку отзыва (похожа на модерацию, но без кнопок и username)
        const card = document.createElement("div");
        card.className = "review-moderation-card"; // Используем тот же стиль карточки

        // Левая часть с названием рецепта и текстом отзыва
        const cardLeft = document.createElement("div");
        cardLeft.className = "card-left";

        const recipeLink = document.createElement("a");
        recipeLink.href = `recipe.html?recipe_id=${review.recipe_id}`;
        recipeLink.textContent = `рецепт "${recipe.title}"`;

        const reviewText = document.createElement("div");
        reviewText.textContent = review.content;

        cardLeft.appendChild(recipeLink);
        cardLeft.appendChild(reviewText);

        // Рейтинг
        const cardRating = document.createElement("div");
        cardRating.className = "card-rating";
        const star = document.createElement("span");
        star.className = "star";
        star.textContent = "★";
        const ratingVal = document.createElement("span");
        ratingVal.textContent = review.rating.toFixed(1);
        cardRating.appendChild(star);
        cardRating.appendChild(ratingVal);

        // Добавляем в карточку
        card.appendChild(cardLeft);
        card.appendChild(cardRating);

        userReviewsContainer.appendChild(card);
      }
    }
  } catch (error) {
    console.error(error);
    userReviewsContainer.textContent = "Не удалось загрузить ваши отзывы.";
  }

  // Логика выхода
  const logoutBtn = document.getElementById("logout-btn");
  logoutBtn.addEventListener("click", async () => {
    try {
      const response = await fetch(`${BASE_URL}/api/token/`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      // Независимо от ответа, очищаем локальное хранилище и редиректим
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("role_name");

      window.location.href = "index.html";
    } catch (error) {
      console.error("Ошибка при выходе:", error);
      // Даже при ошибке попробуем очистить и редиректить
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("role_name");
      window.location.href = "index.html";
    }
  });
});
