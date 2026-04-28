<template>
  <header class="app-header">
    <div class="header-bg" />
    <div class="header-left">
      <el-button text @click="appStore.toggleSidebar" class="collapse-btn">
        <el-icon :size="18"><Fold v-if="!appStore.sidebarCollapsed" /><Expand v-else /></el-icon>
      </el-button>
      <el-breadcrumb separator="/" class="header-breadcrumb">
        <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="route.meta.title">{{ route.meta.title }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="header-center">
      <span class="env-hint">🌡 温度 24°C · 湿度 52%</span>
    </div>
    <div class="header-right">
      <span class="header-time">{{ currentTime }}</span>
      <el-tooltip content="通知" placement="bottom">
        <el-button text class="header-icon-btn">
          <el-icon :size="18"><Bell /></el-icon>
          <span class="notif-dot" />
        </el-button>
      </el-tooltip>
      <el-dropdown trigger="click">
        <span class="user-info">
          <el-avatar :size="32" class="user-avatar">{{ authStore.user?.name?.[0] || '管' }}</el-avatar>
          <span class="user-name">{{ authStore.user?.name || '管理员' }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()
const authStore = useAuthStore()
const currentTime = ref('')

let timer
function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false
  })
}
onMounted(() => { updateTime(); timer = setInterval(updateTime, 1000) })
onUnmounted(() => clearInterval(timer))

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-bottom: 1px solid rgba(217, 197, 167, 0.4);
}
.header-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(247,244,235,0.5) 0%, rgba(255,255,255,0.8) 100%);
  pointer-events: none;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  z-index: 1;
}
.collapse-btn {
  color: var(--color-text-secondary);
  transition: color 0.2s;
}
.collapse-btn:hover { color: var(--color-primary); }
.header-breadcrumb :deep(.el-breadcrumb__inner) { font-size: 13px; }
.header-center {
  position: relative;
  z-index: 1;
}
.env-hint {
  font-size: 12px;
  color: var(--color-text-muted);
  letter-spacing: 0.5px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
}
.header-time {
  font-family: 'Inter', monospace;
  font-size: 13px;
  color: var(--color-text-secondary);
  letter-spacing: 0.5px;
}
.header-icon-btn {
  color: var(--color-text-secondary);
  position: relative;
}
.notif-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 6px;
  height: 6px;
  background: var(--color-primary);
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.8);
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 20px;
  transition: background 0.2s;
}
.user-info:hover {
  background: var(--bg-row-hover);
}
.user-avatar {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark)) !important;
  color: var(--color-white) !important;
  font-family: 'Noto Serif SC', serif;
  font-weight: 700;
}
.user-name {
  font-size: 13px;
  color: var(--color-text);
  font-weight: 500;
}
</style>
