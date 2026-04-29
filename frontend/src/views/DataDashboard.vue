<template>
  <div class="data-dashboard">
    <div class="page-header">
      <div>
        <h2>数据大屏</h2>
        <p class="header-subtitle">全平台质量数据实时监控</p>
      </div>
      <div class="header-actions">
        <span class="live-badge">
          <span class="live-dot" /> 实时监控
        </span>
        <el-button text @click="toggleFullscreen">
          <el-icon :size="18"><FullScreen /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- KPI Row -->
    <el-row :gutter="20" class="kpi-row">
      <el-col :span="6" v-for="kpi in kpis" :key="kpi.label">
        <div class="kpi-card">
          <span class="kpi-label">{{ kpi.label }}</span>
          <div class="kpi-value-row">
            <span class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</span>
            <span class="kpi-unit">{{ kpi.unit }}</span>
          </div>
          <span v-if="kpi.sub" class="kpi-sub">{{ kpi.sub }}</span>
        </div>
      </el-col>
    </el-row>

    <!-- Charts Row 1 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <div class="rose-card">
          <div class="card-header">缺陷类型分布</div>
          <div class="card-body">
            <v-chart :option="defectChartOption" style="height: 340px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="rose-card">
          <div class="card-header">本周质检趋势</div>
          <div class="card-body">
            <v-chart :option="trendChartOption" style="height: 340px" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- Charts Row 2 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="8">
        <div class="rose-card">
          <div class="card-header">售后问题分布</div>
          <div class="card-body">
            <v-chart :option="afterSalesChartOption" style="height: 280px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="rose-card">
          <div class="card-header">产品等级占比</div>
          <div class="card-body">
            <v-chart :option="gradeChartOption" style="height: 280px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="rose-card">
          <div class="card-header">今日质检状态</div>
          <div class="card-body">
            <v-chart :option="statusChartOption" style="height: 280px" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchDashboardStats } from '@/api'
import type { DashboardStats } from '@/types'
import VChart from 'vue-echarts'

const stats = ref<DashboardStats | null>(null)
const kpis = ref<{ label: string; value: string | number; color: string; unit: string; sub: string }[]>([])

onMounted(async () => {
  const res = await fetchDashboardStats()
  stats.value = res.data
  kpis.value = [
    { label: '今日质检', value: res.data.todayInspections, color: '#8B4513', unit: '件', sub: '较昨日 +8.3%' },
    { label: '异常产品', value: res.data.anomalyCount, color: '#D4913E', unit: '件', sub: '较昨日 -12.5%' },
    { label: '质检通过率', value: res.data.passRate + '%', color: '#4A7C59', unit: '', sub: '高于目标 3.5%' },
    { label: '产品总数', value: res.data.totalProducts, color: '#B8944B', unit: '件', sub: '累计建档' },
  ]
})

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

const tooltipStyle: Record<string, unknown> = {
  backgroundColor: '#FFFFFF',
  borderColor: '#E8E0D5',
  borderWidth: 1,
  padding: [12, 16],
  textStyle: { color: '#1E1812', fontSize: 13 }
}

const defectChartOption = computed(() => ({
  tooltip: {
    ...tooltipStyle,
    trigger: 'axis',
    formatter: (params: any[]) => {
      const item = params[0]
      const total = stats.value?.defectDistribution?.reduce((a, b) => a + b.value, 0) || 1
      const pct = ((item.value / total) * 100).toFixed(1)
      return `<b>${item.name}</b><br/>数量: ${item.value}<br/>占比: ${pct}%`
    }
  },
  grid: { left: 48, right: 24, bottom: 36, top: 16 },
  xAxis: {
    type: 'category',
    data: stats.value?.defectDistribution?.map(d => d.name) || [],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#9B8E7E', fontSize: 11 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#F0EBE2', type: 'dashed' } },
    axisLabel: { color: '#9B8E7E' }
  },
  series: [{
    type: 'bar',
    data: (stats.value?.defectDistribution || []).map((d, i) => ({
      value: d.value,
      itemStyle: {
        color: ['#8B4513', '#A0724A', '#B8944B', '#C4A882', '#D4BD8C', '#6B5E4E', '#4A7C59'][i],
        borderRadius: [6, 6, 0, 0]
      }
    })),
    barWidth: 28,
    barMaxWidth: 44,
    label: { show: true, position: 'top', color: '#1E1812', fontSize: 11, fontWeight: 600 }
  }]
}))

const trendChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'axis' },
  legend: {
    data: ['检测数', '合格数'],
    bottom: 0,
    icon: 'roundRect',
    itemWidth: 10,
    itemHeight: 4,
    textStyle: { color: '#6B5E4E', fontSize: 12 }
  },
  grid: { left: 48, right: 16, bottom: 44, top: 16 },
  xAxis: {
    type: 'category',
    data: stats.value?.weeklyTrend?.map(t => t.date) || [],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#9B8E7E', fontSize: 11 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#F0EBE2', type: 'dashed' } },
    axisLabel: { color: '#9B8E7E' }
  },
  series: [
    {
      name: '检测数',
      type: 'bar',
      data: stats.value?.weeklyTrend?.map(t => t.count) || [],
      barWidth: 20,
      barGap: '30%',
      itemStyle: { color: '#D4BD8C', borderRadius: [4,4,0,0] }
    },
    {
      name: '合格数',
      type: 'line',
      data: stats.value?.weeklyTrend?.map(t => t.pass) || [],
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { color: '#8B4513', width: 2.5 },
      itemStyle: { color: '#8B4513', borderColor: '#FFFFFF', borderWidth: 3 },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(139,69,19,0.10)' },
            { offset: 1, color: 'rgba(139,69,19,0.01)' }
          ]
        }
      }
    }
  ]
}))

const pieBase = {
  type: 'pie',
  radius: ['45%', '72%'],
  padAngle: 2,
  itemStyle: { borderRadius: 8, borderColor: '#FFFFFF', borderWidth: 2 },
  label: { formatter: '{b}\n{d}%', fontSize: 11, color: '#1E1812', lineHeight: 16 },
  labelLine: { lineStyle: { color: '#D4BD8C' } }
}

const afterSalesChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c}件 ({d}%)' },
  series: [{
    ...pieBase,
    data: stats.value?.afterSalesTypes || [],
    color: ['#8B4513', '#A0724A', '#B8944B', '#C4A882']
  }]
}))

const gradeChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c}件 ({d}%)' },
  series: [{
    ...pieBase,
    data: [
      { name: 'A 级', value: 98 },
      { name: 'B 级', value: 42 },
      { name: 'C 级', value: 16 }
    ],
    color: ['#4A7C59', '#B8944B', '#8B4513']
  }]
}))

const statusChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c}件' },
  series: [{
    ...pieBase,
    data: [
      { name: '已完成', value: 16 },
      { name: '进行中', value: 5 },
      { name: '待处理', value: 3 }
    ],
    color: ['#4A7C59', '#B8944B', '#D4913E']
  }]
}))
</script>

<style scoped>
.data-dashboard {
  max-width: 1440px;
  margin: 0 auto;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}
.page-header h2 {
  font-size: 24px;
  letter-spacing: 0.04em;
}
.header-subtitle {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-green);
  background: var(--color-green-bg);
  padding: 5px 14px;
  border-radius: 20px;
}
.live-dot {
  width: 7px;
  height: 7px;
  background: var(--color-green);
  border-radius: 50%;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.75); }
}

.kpi-row { margin-bottom: 20px; }
.charts-row { margin-bottom: 20px; }

.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--card-radius);
  padding: 22px 24px;
  box-shadow: var(--shadow-card);
  transition: box-shadow 0.3s var(--ease-out-expo), transform 0.3s var(--ease-out-expo);
  contain: layout style;
}
.kpi-card:hover {
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-2px);
}
.kpi-label {
  font-size: 12px;
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  font-weight: 500;
}
.kpi-value-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin: 8px 0 4px;
}
.kpi-value {
  font-family: 'Inter', sans-serif;
  font-size: 38px;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.kpi-unit {
  font-size: 13px;
  color: var(--color-text-secondary);
}
.kpi-sub {
  font-size: 11px;
  color: var(--color-text-muted);
}
</style>
