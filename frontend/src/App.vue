<template>
  <router-view v-slot="{ Component, route }">
    <Transition name="fade-slide" mode="out-in">
      <component :is="Component" :key="route.path" />
    </Transition>
  </router-view>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

onMounted(() => {
  const root = document.documentElement
  const tokens: Record<string, string> = {
    '--el-color-primary': '#8B4513',
    '--el-color-primary-dark-2': '#6B3410',
    '--el-color-primary-light-3': '#A0724A',
    '--el-color-primary-light-5': '#C4A882',
    '--el-color-primary-light-7': '#D4BD8C',
    '--el-color-primary-light-8': '#E8D5C0',
    '--el-color-primary-light-9': '#F5EEE5',
    '--el-color-primary-light-10': '#FDF6F0',
    '--el-color-success': '#4A7C59',
    '--el-color-warning': '#D4913E',
    '--el-color-danger': '#C0392B',
    '--el-color-info': '#9B8E7E',
    '--el-border-radius-base': '10px',
    '--el-font-size-base': '14px',
    '--el-font-family': "'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif",
  }
  Object.entries(tokens).forEach(([key, val]) => root.style.setProperty(key, val))
  appStore.initApp()
})
</script>
