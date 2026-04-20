<template>
  <v-container v-if="user">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card title="Личный кабинет" subtitle="Управление доступом" variant="outlined">
          <v-card-text>
            <div class="mb-6">
              <div class="text-caption">Ваш текущий ключ активации:</div>
              <div class="d-flex align-center">
                <code class="text-h5 primary--text">{{ user.activation_key || 'Ключ уже использован' }}</code>
                <v-btn icon="mdi-refresh" variant="text" class="ml-2" @click="refreshKey" :loading="keyLoading" />
              </div>
              <div class="text-grey text-caption mt-1">* Обновление ключа аннулирует старый и отправит новый на почту</div>
            </div>

            <v-divider class="my-4"></v-divider>

            <h3 class="mb-4">Смена пароля</h3>
            <v-form @submit.prevent="changePassword">
              <v-text-field v-model="passForm.newPassword" label="Новый пароль" type="password" />
              <v-btn type="submit" variant="tonal" color="secondary">Сменить пароль</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref(null)
const keyLoading = ref(false)
const passForm = ref({ newPassword: '' })

const fetchProfile = async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get('http://localhost:8000/api/me', {
    headers: { Authorization: `Bearer ${token}` }
  })
  user.value = res.data
}

const refreshKey = async () => {
  keyLoading.value = true
  try {
    await axios.post('http://localhost:8000/api/users/refresh-key', {}, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    await fetchProfile()
    alert("Новый ключ сгенерирован и отправлен на почту!")
  } catch (err) {
    console.error(err)
  } finally {
    keyLoading.value = false
  }
}

onMounted(fetchProfile)
</script>