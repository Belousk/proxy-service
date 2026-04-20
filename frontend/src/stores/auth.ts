import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null as any
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async fetchProfile() {
      const res = await axios.get('http://localhost:8000/api/users/me', {
        headers: { Authorization: `Bearer ${this.token}` }
      })
      this.user = res.data
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})