<template>
  <div class="not-found">
    <div class="not-found-content">
      <span class="code">404</span>
      <h2>页面未找到</h2>
      <p>您访问的页面不存在或已被移除</p>
      <el-button type="primary" size="large" @click="$router.push('/dashboard')">返回工作台</el-button>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-main);
}
.not-found-content { text-align: center; }
.code {
  font-family: 'Inter', sans-serif;
  font-size: 96px;
  font-weight: 800;
  color: var(--color-primary);
  display: block;
  line-height: 1;
  margin-bottom: 8px;
  letter-spacing: -0.03em;
  opacity: 0.8;
}
.not-found-content h2 { font-size: 20px; color: var(--color-text); margin-bottom: 8px; }
.not-found-content p { font-size: 14px; color: var(--color-text-muted); margin-bottom: 24px; }
</style>
