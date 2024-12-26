const BASE_URL = "http://localhost:8080";

async function request(
  endpoint,
  method = "GET",
  data = null,
  needsAuth = false,
) {
  const headers = { "Content-Type": "application/json" };

  if (needsAuth) {
    const token = localStorage.getItem("token");
    if (token) {
      headers["Authorization"] = token;
    }
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers,
    body: data ? JSON.stringify(data) : null,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText);
  }

  return response.json();
}

// Получение токена авторизации
async function getToken(username, password) {
  return await request("/api/token/", "POST", { username, password }, false);
}

// Регистрация пользователя
async function registerUser(username, password) {
  // Возвращаем промис, если 201 Created - всё хорошо. Иначе выбросит ошибку.
  return await request("/api/user/", "POST", { username, password }, false);
}

export { getToken, registerUser };
