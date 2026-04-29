<template>
  <aside class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
    <!-- Brand -->
    <div class="sidebar-brand">
      <div class="brand-logo">
        <span class="logo-mark">匠</span>
      </div>
      <Transition name="fade">
        <div v-show="!appStore.sidebarCollapsed" class="brand-text">
          <span class="brand-name">匠木云检</span>
          <span class="brand-desc">智能质检与溯源平台</span>
        </div>
      </Transition>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ active: isActive(item.path) }"
        :title="appStore.sidebarCollapsed ? item.title : ''"
      >
        <span class="nav-icon">
          <el-icon :size="19"><component :is="item.icon" /></el-icon>
        </span>
        <span class="nav-label">{{ item.title }}</span>
        <span v-if="isActive(item.path)" class="nav-indicator" />
      </router-link>
    </nav>

    <!-- Footer -->
    <Transition name="fade">
      <div v-show="!appStore.sidebarCollapsed" class="sidebar-footer">
        <div class="footer-avatar">
          <span>{{ authStore.user?.name?.[0] || '管' }}</span>
        </div>
        <div class="footer-info">
          <p class="footer-name">{{ authStore.user?.name || '管理员' }}</p>
          <p class="footer-role">质量管理员</p>
        </div>
      </div>
    </Transition>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const appStore = useAppStore()
const authStore = useAuthStore()

interface MenuItem {
  path: string
  title: string
  icon: string
}

const menuItems: MenuItem[] = [
  { path: '/dashboard', title: '工作台', icon: 'DataBoard' },
  { path: '/products', title: '产品档案', icon: 'Goods' },
  { path: '/inspection', title: 'AI 质检', icon: 'Camera' },
  { path: '/warehouse', title: '出入库管理', icon: 'Box' },
  { path: '/reports', title: '质检报告', icon: 'Document' },
  { path: '/after-sales', title: '售后管理', icon: 'Service' },
  { path: '/data-dashboard', title: '数据大屏', icon: 'DataAnalysis' },
]

function isActive(path: string) {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--bg-sidebar);
  z-index: 100;
  transition: width 0.28s var(--ease-out-expo);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--color-border);
  box-shadow: var(--shadow-sidebar);
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

/* Brand */
.sidebar-brand {
  padding: 20px 18px 16px;
  display: flex;
  align-items: center;
  gap: 0;
  flex-shrink: 0;
}
.brand-logo {
  flex-shrink: 0;
}
.logo-mark {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--color-primary), #A0522D);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #FFFFFF;
  font-family: 'Noto Serif SC', serif;
  font-weight: 900;
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.25);
}
.brand-text {
  margin-left: 14px;
  min-width: 0;
  overflow: hidden;
}
.brand-name {
  display: block;
  font-family: 'Noto Serif SC', serif;
  font-size: 19px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: 0.06em;
  white-space: nowrap;
}
.brand-desc {
  display: block;
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 2px;
  white-space: nowrap;
  letter-spacing: 0.03em;
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  padding: 8px 10px;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.nav-item {
  display: flex;
  align-items: center;
  height: 44px;
  padding: 0 12px;
  border-radius: 10px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all 0.2s var(--ease-in-out);
  position: relative;
  gap: 12px;
  cursor: pointer;
}
.nav-item:hover {
  background: var(--bg-sidebar-hover);
  color: var(--color-text);
}
.nav-item.active {
  background: var(--bg-sidebar-active);
  color: var(--color-primary);
  font-weight: 600;
}
.nav-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
}
.nav-item.active .nav-icon {
  color: var(--color-primary);
}
.nav-label {
  font-size: 14px;
  white-space: nowrap;
  letter-spacing: 0.03em;
}
.nav-indicator {
  position: absolute;
  right: 12px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
}

/* Footer */
.sidebar-footer {
  padding: 14px 18px;
  border-top: 1px solid var(--color-border-light);
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.footer-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--color-primary), #A0522D);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  color: #FFFFFF;
  font-family: 'Noto Serif SC', serif;
  font-weight: 700;
  flex-shrink: 0;
}
.footer-info {
  min-width: 0;
}
.footer-name {
  font-size: 13px;
  color: var(--color-text);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.footer-role {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 1px;
}

/* Collapsed state */
.collapsed .sidebar-nav {
  padding: 8px 6px;
}
.collapsed .nav-item {
  justify-content: center;
  padding: 0;
  gap: 0;
}
.collapsed .nav-indicator {
  right: 4px;
  width: 4px;
  height: 4px;
}
.collapsed .sidebar-brand {
  padding: 20px 14px 12px;
}
.collapsed .sidebar-footer {
  display: none;
}

/* Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s var(--ease-in-out);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
