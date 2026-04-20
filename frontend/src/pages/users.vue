<template>
  <v-container>
    <h2 class="text-h5 font-weight-bold mb-6">Зарегистрированные пользователи</h2>
    
    <v-card variant="outlined">
      <v-table theme="dark">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Ключ активации</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>
              <code class="text-amber-lighten-3" v-if="user.activation_key">{{ user.activation_key }}</code>
              <v-chip v-else size="x-small" color="grey">Использован</v-chip>
            </td>
            <td>
              <v-icon :color="user.is_active ? 'success' : 'error'">
                {{ user.is_active ? 'mdi-check-circle' : 'mdi-minus-circle' }}
              </v-icon>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])

onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/users/list')
  users.value = res.data
})
</script>