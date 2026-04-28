<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-brand">
        <div class="brand-icon">匠</div>
        <h1 class="brand-title">匠木云检</h1>
        <p class="brand-subtitle">智能质检与溯源平台</p>
      </div>
      <el-card class="login-card" shadow="never">
        <h2 class="login-title">用户登录</h2>
        <el-form ref="formRef" :model="form" :rules="rules" @keyup.enter="handleLogin">
          <el-form-item prop="username">
            <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" size="large" />
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" placeholder="密码" :prefix-icon="Lock" size="large" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="large" class="login-btn" :loading="loading" @click="handleLogin">
              登 录
            </el-button>
          </el-form-item>
        </el-form>
        <p class="login-hint">演示账号：admin / admin123</p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({ username: 'admin', password: 'admin123' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    router.push('/dashboard')
  } catch {
    ElMessage.error('登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #5C3A21 0%, #8B5E3C 50%, #B8845E 100%);
}
.login-container {
  display: flex;
  align-items: center;
  gap: 60px;
}
.login-brand {
  text-align: center;
  color: var(--color-white);
}
.brand-icon {
  width: 80px;
  height: 80px;
  background: rgba(255,255,255,0.15);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44px;
  margin: 0 auto 20px;
  backdrop-filter: blur(10px);
}
.brand-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
}
.brand-subtitle {
  font-size: 16px;
  opacity: 0.8;
}
.login-card {
  width: 400px;
  border-radius: 16px;
  padding: 20px;
}
.login-title {
  text-align: center;
  font-size: 20px;
  margin-bottom: 24px;
  color: var(--color-text);
}
.login-btn {
  width: 100%;
  background: var(--color-primary);
  border: none;
}
.login-btn:hover { background: var(--color-primary-dark); }
.login-hint {
  text-align: center;
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 8px;
}
</style>
