<template>
  <div class="stat-card" @click="$emit('click')">
    <div class="stat-body">
      <div class="stat-info">
        <span class="stat-label">{{ label }}</span>
        <div class="stat-value-row">
          <span class="stat-value" :style="{ color: color || 'var(--color-primary)' }">
            {{ value }}
          </span>
          <span v-if="unit" class="stat-unit">{{ unit }}</span>
        </div>
        <span v-if="subtext" class="stat-subtext">{{ subtext }}</span>
      </div>
      <div class="stat-icon" :style="{ background: iconBg || `${color}18` || 'rgba(139,69,19,0.08)' }">
        <el-icon :size="22" :style="{ color: color || 'var(--color-primary)' }">
          <component :is="icon" />
        </el-icon>
      </div>
    </div>
    <div v-if="trend" :class="['stat-trend', trend]">
      <el-icon :size="12">
        <ArrowUp v-if="trend === 'up'" />
        <ArrowDown v-else />
      </el-icon>
      {{ trendPercent }}% vs 昨日
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  unit: String,
  icon: String,
  color: { type: String, default: '#8B4513' },
  iconBg: String,
  trend: String,
  trendPercent: [String, Number],
  subtext: String
})
defineEmits(['click'])
</script>

<style scoped>
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-card);
  padding: 20px 22px;
  cursor: pointer;
  transition: box-shadow 0.3s var(--ease-out-expo),
              transform 0.3s var(--ease-out-expo);
  contain: layout style;
}
.stat-card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}
.stat-body {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.stat-label {
  font-size: 12px;
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-weight: 500;
}
.stat-value-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
}
.stat-value {
  font-family: 'Inter', sans-serif;
  font-size: 36px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.stat-unit {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-weight: 500;
}
.stat-subtext {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 2px;
}
.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  margin-top: 12px;
}
.stat-trend.up {
  background: var(--color-green-bg);
  color: var(--color-green);
}
.stat-trend.down {
  background: var(--color-red-bg);
  color: var(--color-red);
}
</style>
