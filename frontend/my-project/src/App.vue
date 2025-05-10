<template>
  <div id="app">
    <h1>Добро пожаловать!</h1>

    <!-- Проверка на авторизацию -->
    <div v-if="isAuthenticated">
      <p>Вы успешно вошли в систему!</p>
      <button @click="logout">Выйти</button>
    </div>

    <!-- Если не авторизован, показываем формы регистрации или входа -->
    <div v-else>
      <auth-components @auth="handleAuth" />
    </div>
  </div>
</template>

<script>
// Импорт компонента для аутентификации
import AuthComponents from './components/AuthComponents.vue';

export default {
  name: 'App',
  components: {
    AuthComponents,
  },
  data() {
    return {
      isAuthenticated: false, // Статус авторизации
    };
  },
  methods: {
    // Метод для обновления состояния аутентификации
    handleAuth() {
      this.isAuthenticated = true;
    },

    // Метод для выхода
    logout() {
      this.isAuthenticated = false;
    },
  },
};
</script>

<style>
/* Стили для компонента App.vue */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}

h1 {
  color: #42b983;
}

button {
  padding: 10px 20px;
  margin-top: 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #35495e;
}
</style>
