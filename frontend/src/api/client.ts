import axios from 'axios'
import { ElMessage } from 'element-plus'

const client = axios.create({
  baseURL: '',
  timeout: 15000,
})

client.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    const msg = err.response?.data?.detail || err.response?.data?.message || err.message
    ElMessage.error(msg)
    return Promise.reject(err)
  }
)

export default client
