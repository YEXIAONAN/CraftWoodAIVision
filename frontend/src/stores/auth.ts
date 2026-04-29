import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo, LoginResult } from '@/types'
import { loginApi, fetchCurrentUser } from '@/api'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<UserInfo | null>(null)
  const token = ref<string>(localStorage.getItem('token') || '')

  const isLoggedIn = computed(() => !!token.value)
  const userRole = computed(() => user.value?.role || '')

  async function login(username: string, password: string): Promise<LoginResult> {
    const result = await loginApi(username, password)
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

  async function loadUser() {
    const saved = localStorage.getItem('user')
    if (saved) {
      try {
        user.value = JSON.parse(saved) as UserInfo
      } catch {
        user.value = null
      }
    }
    if (token.value) {
      try {
        const res = await fetchCurrentUser()
        user.value = res.data ?? res
        localStorage.setItem('user', JSON.stringify(user.value))
      } catch {
        logout()
      }
    }
  }

  return { user, token, isLoggedIn, userRole, login, logout, loadUser }
})
