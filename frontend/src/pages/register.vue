<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-4">
      <v-card-title class="text-center">Регистрация</v-card-title>
      
      <v-form v-if="!isRegistered" @submit.prevent="register">
        <v-text-field v-model="form.email" label="Email" type="email" required />
        <v-text-field v-model="form.password" label="Пароль" type="password" required />
        <v-text-field v-model="form.confirmPassword" label="Подтвердите пароль" type="password" required />
        <v-btn type="submit" color="primary" block :loading="loading" class="mt-4">Создать аккаунт</v-btn>
      </v-form>

      <v-alert v-else type="success" variant="tonal" class="mt-4">
        Регистрация успешна! Письмо с ключом активации отправлено на вашу почту.
        <v-btn variant="text" to="/login" class="mt-2">Перейти ко входу</v-btn>
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({ email: '', password: '', confirmPassword: '' })
const loading = ref(false)
const isRegistered = ref(false)

const register = async () => {
  // 1. Проверка на фронтенде (для пользователя)
  if (form.value.password !== form.value.confirmPassword) {
    alert("Пароли не совпадают")
    return
  }
  
  loading.value = true
  try {
    // 2. Формируем объект строго по схеме UserCreate
    const payload = {
      email: form.value.email,
      password: form.value.password,
      password_confirm: form.value.confirmPassword // Добавляем это поле!
    }
    
    console.log("Отправка на бэкенд:", payload)
    
    const res = await axios.post('http://localhost:8000/api/register', payload)
    isRegistered.value = true
    
  } catch (err) {
    // Вывод читаемой ошибки из FastAPI
    const errorDetail = err.response?.data?.detail
    if (Array.isArray(errorDetail)) {
      alert("Ошибка валидации: " + errorDetail.map(e => e.msg).join(', '))
    } else {
      alert(errorDetail || "Ошибка регистрации")
    }
  } finally {
    loading.value = false
  }
}
</script>