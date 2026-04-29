<template>
  <div class="login-page">
    <!-- Animated background -->
    <div class="login-bg">
      <div class="bg-orb orb-1" />
      <div class="bg-orb orb-2" />
      <div class="bg-orb orb-3" />
      <div class="bg-grid" />
    </div>

    <div class="login-container">
      <!-- Brand -->
      <div class="login-brand">
        <div class="brand-badge">
          <span>匠</span>
        </div>
        <h1 class="brand-title">匠木云检</h1>
        <p class="brand-desc">AI-Powered Quality Inspection &amp; Traceability</p>
        <div class="brand-features">
          <span><span class="dot" />AI 视觉检测</span>
          <span><span class="dot" />全链溯源</span>
          <span><span class="dot" />实时大屏</span>
        </div>
      </div>

      <!-- Card -->
      <div class="login-card">
        <div class="card-header">
          <h2>欢迎回来</h2>
          <p>登录您的管理账户</p>
        </div>
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="form.username"
              placeholder="用户名"
              :prefix-icon="User"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              :prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :loading="loading"
              @click="handleLogin"
            >
              {{ loading ? '验证中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>
        <p class="login-hint">演示账号：admin / admin123</p>
      </div>
    </div>

    <p class="login-footer">© 2026 匠木云检 · 智能质检与溯源平台</p>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, type FormInstance } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({ username: 'admin', password: 'admin123' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    router.push('/dashboard')
  } catch {
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: #1A1410;
}

/* Animated background */
.login-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
  animation: orb-float 20s ease-in-out infinite;
}
.orb-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(139, 69, 19, 0.5), transparent);
  top: -15%;
  right: -10%;
  animation-delay: 0s;
}
.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(184, 148, 75, 0.4), transparent);
  bottom: -15%;
  left: -8%;
  animation-delay: -7s;
}
.orb-3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(139, 69, 19, 0.3), transparent);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -14s;
}
@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-15px, 25px) scale(0.95); }
  75% { transform: translate(-25px, -15px) scale(1.02); }
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* Container */
.login-container {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 80px;
}

/* Brand */
.login-brand {
  color: #FFFFFF;
  text-align: center;
  max-width: 300px;
}
.brand-badge {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42px;
  font-family: 'Noto Serif SC', serif;
  font-weight: 900;
}
.brand-title {
  font-size: 38px;
  font-weight: 700;
  font-family: 'Noto Serif SC', serif;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
}
.brand-desc {
  font-size: 13px;
  opacity: 0.55;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 28px;
}
.brand-features {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}
.brand-features span {
  font-size: 12px;
  opacity: 0.6;
  display: flex;
  align-items: center;
  gap: 6px;
}
.brand-features .dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
}

/* Card */
.login-card {
  width: 400px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 36px 32px 28px;
}
.card-header {
  text-align: center;
  margin-bottom: 28px;
}
.card-header h2 {
  color: #FFFFFF;
  font-size: 22px;
  margin-bottom: 6px;
}
.card-header p {
  color: rgba(255, 255, 255, 0.45);
  font-size: 13px;
}

/* Form overrides for dark background */
.login-card :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  box-shadow: none !important;
  border-radius: 10px !important;
  padding: 4px 14px !important;
}
.login-card :deep(.el-input__inner) {
  color: #FFFFFF !important;
  font-size: 14px;
}
.login-card :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}
.login-card :deep(.el-input__prefix .el-icon) {
  color: rgba(255, 255, 255, 0.3);
}
.login-card :deep(.el-input__suffix .el-icon) {
  color: rgba(255, 255, 255, 0.3);
}
.login-card :deep(.el-input__wrapper:hover) {
  border-color: rgba(255, 255, 255, 0.25) !important;
}
.login-card :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(255, 255, 255, 0.4) !important;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.06) !important;
}

.login-btn {
  width: 100%;
  height: 46px !important;
  border-radius: 10px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  letter-spacing: 0.1em !important;
  background: linear-gradient(135deg, #A0522D, #8B4513) !important;
  border: none !important;
  margin-top: 4px;
  transition: all 0.3s var(--ease-out-expo) !important;
}
.login-btn:hover {
  background: linear-gradient(135deg, #B5633A, #9B4E1A) !important;
  box-shadow: 0 8px 24px rgba(139, 69, 19, 0.4) !important;
  transform: translateY(-1px);
}

.login-hint {
  text-align: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
  margin-top: 16px;
}

/* Footer */
.login-footer {
  position: relative;
  z-index: 2;
  color: rgba(255, 255, 255, 0.2);
  font-size: 12px;
  margin-top: 40px;
  letter-spacing: 0.04em;
}
</style>
