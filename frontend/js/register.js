import { getToken, registerUser } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  // Проверка токена при загрузке страницы
  const existingToken = localStorage.getItem("token");
  if (existingToken) {
    window.location.href = "index.html";
    return; // не продолжаем инициализацию
  }

  const form = document.querySelector(".register-form-container form");
  const errorMessage = document.getElementById("error-message");

  form.addEventListener("submit", async (e) => {
    const username = form.querySelector("#reg_username").value.trim();
    const pass = form.querySelector("#reg_password").value.trim();
    const passConfirm = form
      .querySelector("#reg_password_confirm")
      .value.trim();

    if (pass !== passConfirm) {
      e.preventDefault();
      errorMessage.textContent = "Пароли должны совпадать";
      errorMessage.style.display = "block";
      return;
    } else {
      errorMessage.style.display = "none";
    }

    e.preventDefault(); // Предотвратим стандартную отправку формы

    try {
      // Регистрация
      await registerUser(username, pass);

      // Авторизация после успешной регистрации
      const token = await getToken(username, pass);
      localStorage.setItem("token", token);

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

      errorMessage.style.display = "none";
      window.location.href = "index.html";
    } catch (error) {
      const msg = error.message;
      let displayError = "Произошла ошибка при регистрации";

      if (msg.includes("already exist")) {
        displayError = `Пользователь ${username} уже существует`;
      }

      errorMessage.textContent = displayError;
      errorMessage.style.display = "block";
    }
  });
});
