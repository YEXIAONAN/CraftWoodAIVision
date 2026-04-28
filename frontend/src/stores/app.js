import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const breadcrumbs = ref([])

  function initApp() {
    const saved = localStorage.getItem('sidebarCollapsed')
    if (saved) sidebarCollapsed.value = JSON.parse(saved)
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
    localStorage.setItem('sidebarCollapsed', JSON.stringify(sidebarCollapsed.value))
  }

  function setBreadcrumbs(paths) {
    breadcrumbs.value = paths
  }

  return { sidebarCollapsed, breadcrumbs, initApp, toggleSidebar, setBreadcrumbs }
})
