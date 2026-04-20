<template>
  <v-container>
    <div class="d-flex justify-space-between align-center mb-6">
      <h1 class="text-h4">Управление прокси</h1>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="dialog = true">
        Добавить сервер
      </v-btn>
    </div>

    <v-row>
      <v-col v-for="vm in vms" :key="vm.id" cols="12" sm="6" md="4">
        <v-card border flat>
          <v-card-item>
            <v-card-title>{{ vm.name }}</v-card-title>
            <v-card-subtitle>{{ vm.host }}:{{ vm.port }}</v-card-subtitle>
          </v-card-item>
          
          <v-card-text>
            <v-chip :color="vm.is_active ? 'success' : 'error'" size="small">
              {{ vm.is_active ? 'Активен' : 'Отключен' }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500">
      <v-card title="Новый сервер">
        <v-card-text>
          <v-text-field v-model="newVm.name" label="Название" placeholder="NL-Proxy-1" />
          <v-text-field v-model="newVm.host" label="IP адрес / Хост" />
          <v-text-field v-model.number="newVm.port" label="Порт" type="number" />
          <v-select v-model="newVm.protocol" :items="['socks5', 'http', 'https']" label="Протокол" />
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn text="Отмена" @click="dialog = false" />
          <v-btn color="primary" :loading="loading" @click="addServer">Создать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const vms = ref([])
const dialog = ref(false)
const loading = ref(false)

const initialForm = { name: '', host: '', port: 1080, protocol: 'socks5' }
const newVm = ref({ ...initialForm })

const fetchVms = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/proxy/list')
    vms.value = res.data
  } catch (err) {
    console.error("Ошибка загрузки:", err)
  }
}

const addServer = async () => {
  if (!newVm.value.name || !newVm.value.host) return
  
  loading.value = true
  try {
    await axios.post('http://localhost:8000/api/proxy/create', newVm.value)
    await fetchVms()
    dialog.value = false
    newVm.value = { ...initialForm }
  } catch (err) {
    alert("Ошибка при создании сервера")
  } finally {
    loading.value = false
  }
}

onMounted(fetchVms)
</script>