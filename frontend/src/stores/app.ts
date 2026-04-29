import { defineStore } from 'pinia'
import { ref } from 'vue'

interface BreadcrumbItem {
  title: string
  path?: string
}

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const breadcrumbs = ref<BreadcrumbItem[]>([])

  function initApp() {
    const saved = localStorage.getItem('sidebarCollapsed')
    if (saved) sidebarCollapsed.value = JSON.parse(saved)
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
    localStorage.setItem('sidebarCollapsed', JSON.stringify(sidebarCollapsed.value))
  }

  function setBreadcrumbs(paths: BreadcrumbItem[]) {
    breadcrumbs.value = paths
  }

  return { sidebarCollapsed, breadcrumbs, initApp, toggleSidebar, setBreadcrumbs }
})
