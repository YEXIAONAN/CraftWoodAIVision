<template>
  <div class="rose-stat-card" @click="$emit('click')">
    <div class="card-accent-bar" />
    <div class="card-inner">
      <div class="card-info">
        <span class="card-label">{{ label }}</span>
        <div class="card-value-wrap">
          <span class="card-value num" :style="{ color: color || 'var(--color-primary)' }">{{ value }}</span>
          <span v-if="unit" class="card-unit">{{ unit }}</span>
          <span v-if="trend" :class="['trend', trend]">
            <el-icon :size="14"><ArrowUp v-if="trend === 'up'" /><ArrowDown v-else /></el-icon>
            {{ trendPercent }}%
          </span>
        </div>
        <span v-if="subtext" class="card-subtext">{{ subtext }}</span>
      </div>
      <div class="card-icon-wrap" :style="{ background: `rgba(${iconBg || '155, 58, 28'}, 0.08)` }">
        <el-icon :size="26" :style="{ color: color || 'var(--color-primary)' }">
          <component :is="icon" />
        </el-icon>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  unit: String,
  icon: String,
  color: { type: String, default: '#9B3A1C' },
  iconBg: String,
  trend: String,   // 'up' | 'down'
  trendPercent: [String, Number],
  subtext: String
})
defineEmits(['click'])
</script>

<style scoped>
.rose-stat-card {
  background: var(--bg-card-warm);
  border: 1px solid var(--color-border-card);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(4px);
}
.rose-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
}
.card-accent-bar {
  height: var(--card-accent-height);
  width: 80px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-gold));
  border-radius: 0 0 3px 3px;
}
.card-inner {
  padding: 20px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.card-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.card-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  letter-spacing: 0.5px;
}
.card-value-wrap {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.card-value {
  font-family: 'Inter', sans-serif;
  font-size: 42px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -1px;
}
.card-unit {
  font-size: 13px;
  color: var(--color-text-secondary);
}
.trend {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 12px;
  font-weight: 600;
  padding: 1px 8px;
  border-radius: 10px;
  margin-left: 4px;
}
.trend.up {
  background: rgba(95, 122, 97, 0.12);
  color: var(--color-green-mute);
}
.trend.down {
  background: rgba(155, 58, 28, 0.1);
  color: var(--color-primary);
}
.card-subtext {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 2px;
}
.card-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
