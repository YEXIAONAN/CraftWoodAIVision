<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <p>页面未找到</p>
      <el-button type="primary" @click="$router.push('/dashboard')">返回首页</el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
}
.not-found-content { text-align: center; }
.not-found-content h1 { font-size: 80px; color: var(--color-primary); margin-bottom: 8px; }
.not-found-content p { font-size: 18px; color: var(--color-text-secondary); margin-bottom: 24px; }
</style>
