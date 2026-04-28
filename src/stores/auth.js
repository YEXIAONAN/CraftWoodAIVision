import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { mockLogin, mockCurrentUser } from '@/mock'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  const isLoggedIn = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || '')

  async function login(username, password) {
    const result = await mockLogin(username, password)
    token.value = result.token
    user.value = result.user
    localStorage.setItem('token', result.token)
    localStorage.setItem('user', JSON.stringify(result.user))
    return result
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  function loadUser() {
    const saved = localStorage.getItem('user')
    if (saved) {
      user.value = JSON.parse(saved)
    } else if (token.value) {
      user.value = mockCurrentUser()
    }
  }

  return { user, token, isLoggedIn, userRole, login, logout, loadUser }
})
