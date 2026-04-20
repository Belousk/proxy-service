<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-4" elevation="8">
      <v-card-title class="text-center text-h5 mb-4">Вход в систему</v-card-title>
      
      <v-form @submit.prevent="handleLogin">
        <v-text-field
          v-model="form.username"
          label="Email"
          prepend-inner-icon="mdi-email"
          type="email"
          variant="outlined"
          required
        />

        <v-text-field
          v-model="form.password"
          label="Пароль"
          prepend-inner-icon="mdi-lock"
          type="password"
          variant="outlined"
          required
        />

        <v-btn
          type="submit"
          color="primary"
          block
          size="large"
          :loading="loading"
          class="mt-4"
        >
          Войти
        </v-btn>

        <div class="text-center mt-4">
          <span class="text-grey">Нет аккаунта? </span>
          <router-link to="/register" class="text-decoration-none text-primary">
            Зарегистрироваться
          </router-link>
        </div>
      </v-form>

      <v-alert
        v-if="error"
        type="error"
        variant="tonal"
        class="mt-4"
        closable
      >
        {{ error }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const error = ref(null)

const form = ref({
  username: '', // FastAPI по стандарту OAuth2 ожидает поле 'username'
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Формируем данные как FormData (стандарт для FastAPI OAuth2)
    const formData = new FormData()
    formData.append('username', form.value.username)
    formData.append('password', form.value.password)

    const res = await axios.post('http://localhost:8000/api/login', formData)
    
    // Сохраняем токен
    const token = res.data.access_token
    localStorage.setItem('token', token)
    
    // Устанавливаем заголовок по умолчанию для всех будущих запросов axios
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

    // Переходим в профиль
    router.push('/profile')
  } catch (err) {
    error.value = err.response?.data?.detail || "Неверный логин или пароль"
  } finally {
    loading.value = false
  }
}
</script>