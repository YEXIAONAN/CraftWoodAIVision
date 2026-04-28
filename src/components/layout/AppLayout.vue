<template>
  <div class="app-layout">
    <AppSidebar />
    <div class="app-main" :class="{ collapsed: appStore.sidebarCollapsed }">
      <AppHeader />
      <main class="app-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'

const appStore = useAppStore()
const authStore = useAuthStore()

onMounted(() => {
  authStore.loadUser()
})
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}
.app-main {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s;
  min-width: 0;
}
.app-main.collapsed {
  margin-left: 64px;
}
.app-content {
  flex: 1;
  padding: 24px;
  background: var(--color-bg);
  overflow-y: auto;
}
</style>
