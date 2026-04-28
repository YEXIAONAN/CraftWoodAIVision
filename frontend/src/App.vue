<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

onMounted(() => {
  // Override Element Plus theme tokens for red-wood palette
  const root = document.documentElement
  const tokens = {
    '--el-color-primary': '#9B3A1C',
    '--el-color-primary-dark-2': '#752C12',
    '--el-color-primary-light-3': '#BC6F45',
    '--el-color-primary-light-5': '#D09C6A',
    '--el-color-primary-light-7': '#E4C59E',
    '--el-color-primary-light-8': '#EADBC6',
    '--el-color-primary-light-9': '#F0EAE1',
    '--el-color-primary-light-10': '#FDF6F0',
    '--el-color-success': '#5F7A61',
    '--el-color-warning': '#CF9F5A',
    '--el-color-danger': '#9B3A1C',
    '--el-color-info': '#A6937C',
    '--el-border-radius-base': '12px',
    '--el-font-size-base': '14px',
    '--el-font-family': "'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif",
  }
  Object.entries(tokens).forEach(([key, val]) => root.style.setProperty(key, val))

  appStore.initApp()
})
</script>
