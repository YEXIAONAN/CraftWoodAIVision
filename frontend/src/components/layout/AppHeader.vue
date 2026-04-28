<template>
  <header class="app-header">
    <div class="header-left">
      <button class="collapse-btn" @click="appStore.toggleSidebar">
        <el-icon :size="18">
          <Fold v-if="!appStore.sidebarCollapsed" />
          <Expand v-else />
        </el-icon>
      </button>
      <el-breadcrumb separator="·" class="header-breadcrumb">
        <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="route.meta.title && !route.meta.hidden">
          {{ route.meta.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="header-right">
      <span class="header-time">{{ currentTime }}</span>
      <el-tooltip content="通知中心" placement="bottom">
        <button class="icon-btn">
          <el-icon :size="18"><Bell /></el-icon>
          <span class="notif-dot" />
        </button>
      </el-tooltip>
      <el-dropdown trigger="click" placement="bottom-end">
        <div class="user-info">
          <div class="user-avatar">{{ authStore.user?.name?.[0] || '管' }}</div>
          <span class="user-name">{{ authStore.user?.name || '管理员' }}</span>
          <el-icon :size="12" class="user-arrow"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>
              <el-icon><User /></el-icon>个人设置
            </el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">
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
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  currentTime.value = `${h}:${m}`
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 30000) // every 30s instead of 1s
})
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
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(12px) saturate(150%);
  -webkit-backdrop-filter: blur(12px) saturate(150%);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-header);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s var(--ease-in-out);
}
.collapse-btn:hover {
  background: var(--bg-sidebar-hover);
  color: var(--color-primary);
}

.header-breadcrumb :deep(.el-breadcrumb__inner) {
  font-size: 13px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-time {
  font-family: 'Inter', monospace;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  letter-spacing: 0.04em;
  font-variant-numeric: tabular-nums;
  padding: 4px 10px;
  background: var(--bg-table-header);
  border-radius: 8px;
}

.icon-btn {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.2s var(--ease-in-out);
}
.icon-btn:hover {
  background: var(--bg-sidebar-hover);
  color: var(--color-text);
}

.notif-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 7px;
  height: 7px;
  background: var(--color-red);
  border-radius: 50%;
  border: 2px solid #FFFFFF;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px 4px 4px;
  border-radius: 10px;
  transition: background 0.2s var(--ease-in-out);
}
.user-info:hover {
  background: var(--bg-sidebar-hover);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--color-primary), #A0522D);
  color: #FFFFFF;
  font-family: 'Noto Serif SC', serif;
  font-weight: 700;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-name {
  font-size: 13px;
  color: var(--color-text);
  font-weight: 500;
}

.user-arrow {
  color: var(--color-text-muted);
  margin-left: 2px;
}
</style>
