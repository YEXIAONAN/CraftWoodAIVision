<template>
  <div class="sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
    <div class="sidebar-header">
      <div class="logo">
        <span class="logo-icon">匠</span>
        <span v-show="!appStore.sidebarCollapsed" class="logo-text">匠木云检</span>
      </div>
      <div v-show="!appStore.sidebarCollapsed" class="logo-subtitle">智能质检与溯源平台</div>
    </div>
    <el-menu
      :default-active="route.path"
      :collapse="appStore.sidebarCollapsed"
      :router="true"
      :unique-opened="true"
      class="sidebar-menu"
    >
      <template v-for="item in menuItems" :key="item.path">
        <el-menu-item :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </template>
    </el-menu>
    <div v-show="!appStore.sidebarCollapsed" class="sidebar-footer">
      <div class="wood-grain" />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const appStore = useAppStore()

const menuItems = [
  { path: '/dashboard', title: '工作台', icon: 'DataBoard' },
  { path: '/products', title: '产品档案', icon: 'Goods' },
  { path: '/inspection', title: 'AI 质检', icon: 'Camera' },
  { path: '/warehouse', title: '出入库管理', icon: 'Box' },
  { path: '/reports', title: '质检报告', icon: 'Document' },
  { path: '/after-sales', title: '售后管理', icon: 'Service' },
  { path: '/data-dashboard', title: '数据大屏', icon: 'DataAnalysis' },
]
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: linear-gradient(180deg, var(--bg-sidebar-start) 0%, var(--bg-sidebar-end) 100%);
  z-index: 100;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 4px 0 20px rgba(60, 30, 15, 0.15);
}
.sidebar::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/src/assets/wood-texture.svg') repeat;
  opacity: 0.12;
  pointer-events: none;
}
.sidebar.collapsed {
  width: 64px;
}
.sidebar-header {
  padding: 20px 16px 12px;
  border-bottom: 1px solid rgba(201, 160, 99, 0.15);
  flex-shrink: 0;
  position: relative;
}
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--color-gold), var(--color-primary));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: var(--color-white);
  font-family: 'Noto Serif SC', serif;
  font-weight: 900;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(155, 58, 28, 0.3);
}
.logo-text {
  color: var(--color-text-inverse);
  font-size: 20px;
  font-family: 'Noto Serif SC', serif;
  font-weight: 700;
  white-space: nowrap;
  letter-spacing: 2px;
}
.logo-subtitle {
  font-size: 11px;
  color: var(--color-gold-light);
  margin-top: 6px;
  margin-left: 52px;
  letter-spacing: 1px;
  opacity: 0.7;
  white-space: nowrap;
}
.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent !important;
  padding: 8px 0;
  overflow-y: auto;
}
.sidebar-menu :deep(.el-menu-item) {
  height: 48px;
  line-height: 48px;
  margin: 2px 8px;
  border-radius: 10px;
  color: rgba(240, 228, 206, 0.7) !important;
  transition: all 0.2s;
}
.sidebar-menu :deep(.el-menu-item .el-icon) {
  color: rgba(240, 228, 206, 0.6);
  font-size: 18px;
}
.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(201, 160, 99, 0.12) !important;
  color: var(--color-text-inverse) !important;
}
.sidebar-menu :deep(.el-menu-item:hover .el-icon) {
  color: var(--color-gold) !important;
}
.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(155, 58, 28, 0.5) 0%, rgba(155, 58, 28, 0.15) 100%) !important;
  color: var(--color-white) !important;
  box-shadow: inset 3px 0 0 var(--color-gold);
}
.sidebar-menu :deep(.el-menu-item.is-active .el-icon) {
  color: var(--color-gold) !important;
}
.sidebar-footer {
  padding: 12px 20px;
  border-top: 1px solid rgba(201, 160, 99, 0.1);
}
.wood-grain {
  height: 4px;
  background: linear-gradient(90deg, transparent, var(--color-gold), transparent);
  border-radius: 2px;
  opacity: 0.3;
}
</style>
