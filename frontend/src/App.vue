<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" theme="dark">
      <v-list-item
        prepend-icon="mdi-shield-check"
        title="Proxy Admin"
        subtitle="v1.0.0"
        class="pa-4"
      ></v-list-item>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item 
          prepend-icon="mdi-server" 
          title="Список серверов" 
          to="/"
        ></v-list-item>
        
        <v-list-item 
          prepend-icon="mdi-account-group" 
          title="Пользователи" 
          to="/users"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar border="bottom" elevation="0">
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-app-bar-title>Управление инфраструктурой</v-app-bar-title>
    </v-app-bar>

    <v-main class="bg-grey-darken-4">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const drawer = ref(true)
</script>