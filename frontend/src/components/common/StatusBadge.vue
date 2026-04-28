<template>
  <span :class="['rose-badge', status]">
    <span class="dot" />
    {{ label }}
  </span>
</template>

<script setup>
defineProps({
  status: String,
  label: String
})
</script>

<style scoped>
.rose-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  padding: 3px 12px;
  border-radius: 20px;
  font-weight: 500;
  letter-spacing: 0.3px;
  line-height: 1.4;
}
.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
/* Risk levels */
.rose-badge.low {
  background: var(--bg-tag-green);
  color: var(--color-green-mute);
}
.rose-badge.low .dot { background: var(--color-green-mute); }

.rose-badge.medium {
  background: var(--bg-tag-amber);
  color: #6B4F1A;
}
.rose-badge.medium .dot { background: #CF9F5A; }

.rose-badge.high {
  background: var(--bg-tag-red);
  color: var(--color-white);
}
.rose-badge.high .dot { background: rgba(255,255,255,0.7); }

/* Statuses */
.rose-badge.已完成 {
  background: var(--bg-tag-green);
  color: var(--color-green-mute);
}
.rose-badge.已完成 .dot { background: var(--color-green-mute); }

.rose-badge.待处理 {
  background: var(--bg-tag-amber);
  color: #6B4F1A;
}
.rose-badge.待处理 .dot { background: #CF9F5A; }

.rose-badge.处理中 {
  background: rgba(64, 158, 255, 0.12);
  color: #1D6FA3;
}
.rose-badge.处理中 .dot { background: #409EFF; }

.rose-badge.已关闭, .rose-badge.已出库, .rose-badge.已归档 {
  background: #F0F0F0;
  color: #7A7A7A;
}
.rose-badge.已关闭 .dot, .rose-badge.已出库 .dot, .rose-badge.已归档 .dot { background: #7A7A7A; }

.rose-badge.已入库 {
  background: var(--bg-tag-green);
  color: var(--color-green-mute);
}
.rose-badge.已入库 .dot { background: var(--color-green-mute); }

.rose-badge.仓储中 {
  background: rgba(64, 158, 255, 0.12);
  color: #1D6FA3;
}
.rose-badge.仓储中 .dot { background: #409EFF; }

.rose-badge.待出库 {
  background: var(--bg-tag-amber);
  color: #6B4F1A;
}
.rose-badge.待出库 .dot { background: #CF9F5A; }
</style>
