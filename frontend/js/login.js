import { getToken } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  // Проверка токена при загрузке страницы
  const existingToken = localStorage.getItem("token");
  if (existingToken) {
    window.location.href = "index.html";
    return; // не продолжаем инициализацию
  }

  const form = document.querySelector(".login-form-container form");
  const errorMessage = document.createElement("div");
  errorMessage.className = "error-message";
  form.appendChild(errorMessage);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = form.querySelector("#username").value.trim();
    const password = form.querySelector("#password").value.trim();

    try {
      const token = await getToken(username, password);
      localStorage.setItem("token", token);
      errorMessage.style.display = "none";

      const userResponse = await fetch("http://localhost:8080/api/user/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!userResponse.ok) {
        const errText = await userResponse.text();
        throw new Error(errText);
      }

      const userData = await userResponse.json();
      localStorage.setItem("username", userData.username);
      localStorage.setItem("role_name", userData.role_name);

      window.location.href = "index.html";
    } catch (error) {
      const msg = error.message;
      let displayError = "Произошла ошибка при авторизации";

      if (msg.includes("does not exist")) {
        displayError = `Пользователь ${username} не существует`;
      } else if (msg.includes("Wrong password")) {
        displayError = `Неверный пароль для пользователя ${username}`;
      }

      errorMessage.textContent = displayError;
      errorMessage.style.display = "block";
    }
  });
});
