<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div>
        <label for="reg-username">Имя пользователя:</label>
        <input type="text" id="reg-username" v-model="username" required />
      </div>
      <div>
        <label for="reg-password">Пароль:</label>
        <input type="password" id="reg-password" v-model="password" required />
      </div>
      <button type="submit">Зарегистрироваться</button>
    </form>

    <h2>Вход</h2>
    <form @submit.prevent="login">
      <div>
        <label for="login-username">Имя пользователя:</label>
        <input type="text" id="login-username" v-model="username" required />
      </div>
      <div>
        <label for="login-password">Пароль:</label>
        <input type="password" id="login-password" v-model="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AuthComponents',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/user', {
          name: this.username,
          password: this.password, // если API принимает пароль
        });
        console.log('Регистрация прошла успешно:', response.data);
        this.$emit('auth'); // можно использовать для уведомления родительского компонента
      } catch (error) {
        console.error('Ошибка при регистрации:', error);
      }
    },

    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/login', {
          username: this.username,
          password: this.password,
        });
        console.log('Вход выполнен успешно:', response.data);
        this.$emit('auth');
      } catch (error) {
        console.error('Ошибка при входе:', error);
      }
    },
  },
};
</script>
