import { defineStore } from 'pinia'
import api from '../api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem('access_token') || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.accessToken,
  },

  actions: {
    async register(username, email, password, password2) {
      const response = await api.post('/accounts/register/', {
        username,
        email,
        password,
        password2,
      })
      return response.data
    },

    async login(username, password) {
      const response = await api.post('/accounts/login/', { username, password })
      this.accessToken = response.data.access
      this.user = response.data.user
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      return response.data
    },

    async logout() {
      try {
        await api.post('/accounts/logout/')
      } catch {}
      this.accessToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },

    async fetchUser() {
      if (!this.accessToken) return
      try {
        const response = await api.get('/accounts/user/')
        this.user = response.data
      } catch {
        this.logout()
      }
    },
  },
})
