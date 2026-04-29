<template>
  <div class="app-layout">
    <AppSidebar />
    <div class="app-main" :class="{ collapsed: appStore.sidebarCollapsed }">
      <AppHeader />
      <main class="app-content">
        <router-view v-slot="{ Component, route }">
          <Transition name="fade-slide" mode="out-in">
            <component :is="Component" :key="route.path" />
          </Transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
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
  transition: margin-left 0.28s var(--ease-out-expo);
  min-width: 0;
}
.app-main.collapsed {
  margin-left: var(--sidebar-collapsed-width);
}
.app-content {
  flex: 1;
  padding: 24px 28px;
  overflow-y: auto;
  background: var(--bg-main);
}
</style>
