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
  background: var(--color-green-bg);
  color: var(--color-green);
}
.rose-badge.low .dot { background: var(--color-green); }

.rose-badge.medium {
  background: var(--color-orange-bg);
  color: #8B6914;
}
.rose-badge.medium .dot { background: var(--color-orange); }

.rose-badge.high {
  background: var(--color-red-bg);
  color: var(--color-red);
}
.rose-badge.high .dot { background: var(--color-red); }

/* Statuses */
.rose-badge.已完成 {
  background: var(--color-green-bg);
  color: var(--color-green);
}
.rose-badge.已完成 .dot { background: var(--color-green); }

.rose-badge.待处理 {
  background: var(--color-orange-bg);
  color: #8B6914;
}
.rose-badge.待处理 .dot { background: var(--color-orange); }

.rose-badge.处理中 {
  background: var(--color-blue-bg);
  color: var(--color-blue);
}
.rose-badge.处理中 .dot { background: var(--color-blue); }

.rose-badge.已关闭, .rose-badge.已出库, .rose-badge.已归档 {
  background: #F2F2F2;
  color: #7A7A7A;
}
.rose-badge.已关闭 .dot, .rose-badge.已出库 .dot, .rose-badge.已归档 .dot { background: #7A7A7A; }

.rose-badge.已入库 {
  background: var(--color-green-bg);
  color: var(--color-green);
}
.rose-badge.已入库 .dot { background: var(--color-green); }

.rose-badge.仓储中 {
  background: var(--color-blue-bg);
  color: var(--color-blue);
}
.rose-badge.仓储中 .dot { background: var(--color-blue); }

.rose-badge.待出库 {
  background: var(--color-orange-bg);
  color: #8B6914;
}
.rose-badge.待出库 .dot { background: var(--color-orange); }
</style>
