<template>
  <div class="data-dashboard">
    <div class="page-header">
      <div class="header-title-wrap">
        <img src="/src/assets/seal-stamp.svg" class="seal-icon" alt="" />
        <div>
          <h2>数据大屏</h2>
          <p class="header-subtitle">全平台质量数据实时监控</p>
        </div>
      </div>
      <div class="header-actions">
        <span class="live-badge">
          <span class="live-dot" /> 实时
        </span>
        <el-button text class="fullscreen-btn" @click="toggleFullscreen">
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
            <span class="kpi-value num" :style="{ color: kpi.color }">{{ kpi.value }}</span>
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
          <div class="card-accent" />
          <div class="card-header">缺陷类型分布</div>
          <div class="card-body">
            <v-chart :option="defectChartOption" style="height: 340px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="rose-card">
          <div class="card-accent" />
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
          <div class="card-accent" />
          <div class="card-header">售后问题分布</div>
          <div class="card-body">
            <v-chart :option="afterSalesChartOption" style="height: 280px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="rose-card">
          <div class="card-accent" />
          <div class="card-header">产品等级占比</div>
          <div class="card-body">
            <v-chart :option="gradeChartOption" style="height: 280px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="rose-card">
          <div class="card-accent" />
          <div class="card-header">今日质检状态</div>
          <div class="card-body">
            <v-chart :option="statusChartOption" style="height: 280px" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { fetchDashboardStats } from '@/api'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart, LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, BarChart, PieChart, LineChart, GridComponent, TooltipComponent, LegendComponent])

const stats = ref(null)
const kpis = ref([])

onMounted(async () => {
  const res = await fetchDashboardStats()
  stats.value = res.data
  kpis.value = [
    { label: '今日质检', value: res.data.todayInspections, color: '#9B3A1C', unit: '件', sub: '较昨日 +8.3%' },
    { label: '异常产品', value: res.data.anomalyCount, color: '#CF9F5A', unit: '件', sub: '较昨日 -12.5%' },
    { label: '质检通过率', value: res.data.passRate + '%', color: '#5F7A61', unit: '', sub: '高于目标 3.5%' },
    { label: '产品总数', value: res.data.totalProducts, color: '#C9A063', unit: '件', sub: '累计建档' },
  ]
})

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

const tooltipStyle = {
  backgroundColor: 'rgba(255,245,235,0.95)',
  borderColor: '#D9C5A7',
  borderWidth: 1,
  textStyle: { color: '#2C2418', fontSize: 12 }
}

const defectChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'axis', formatter: (params) => {
    const item = params[0]
    const total = stats.value?.defectDistribution?.reduce((a, b) => a + b.value, 0) || 1
    const pct = ((item.value / total) * 100).toFixed(1)
    return `<b>${item.name}</b><br/>数量: ${item.value}<br/>占比: ${pct}%`
  }},
  grid: { left: 50, right: 30, bottom: 40, top: 20 },
  xAxis: {
    type: 'category',
    data: stats.value?.defectDistribution?.map(d => d.name) || [],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#7E6B54', fontSize: 11 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#D9CBB8', type: 'dashed' } },
    axisLabel: { color: '#7E6B54' }
  },
  series: [{
    type: 'bar',
    data: (stats.value?.defectDistribution || []).map((d, i) => ({
      value: d.value,
      itemStyle: {
        color: ['#9B3A1C', '#BC6F45', '#D09C6A', '#E4C59E', '#CDB89A', '#A6937C', '#5F7A61'][i],
        borderRadius: [6, 6, 0, 0]
      }
    })),
    barWidth: 28,
    barMaxWidth: 48,
    label: {
      show: true,
      position: 'top',
      color: '#2C2418',
      fontSize: 11,
      fontWeight: 600
    }
  }]
}))

const trendChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'axis' },
  legend: {
    data: ['检测数', '合格数'],
    bottom: 0,
    icon: 'circle',
    itemWidth: 8,
    itemHeight: 8,
    textStyle: { color: '#7E6B54', fontSize: 12 }
  },
  grid: { left: 50, right: 24, bottom: 40, top: 16 },
  xAxis: {
    type: 'category',
    data: stats.value?.weeklyTrend?.map(t => t.date) || [],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#7E6B54', fontSize: 11 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#D9CBB8', type: 'dashed' } },
    axisLabel: { color: '#7E6B54' }
  },
  series: [
    {
      name: '检测数',
      type: 'bar',
      data: stats.value?.weeklyTrend?.map(t => t.count) || [],
      barWidth: 20,
      itemStyle: { color: '#CDB89A', borderRadius: [4,4,0,0] }
    },
    {
      name: '合格数',
      type: 'line',
      data: stats.value?.weeklyTrend?.map(t => t.pass) || [],
      smooth: true,
      symbol: 'diamond',
      symbolSize: 10,
      lineStyle: { color: '#9B3A1C', width: 3 },
      itemStyle: { color: '#9B3A1C', borderColor: '#F7F4EB', borderWidth: 2 },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(155,58,28,0.12)' },
            { offset: 1, color: 'rgba(155,58,28,0.01)' }
          ]
        }
      }
    }
  ]
}))

const afterSalesChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c}件 ({d}%)' },
  series: [{
    type: 'pie',
    radius: ['42%', '70%'],
    padAngle: 2,
    itemStyle: { borderRadius: 6 },
    data: stats.value?.afterSalesTypes || [],
    color: ['#9B3A1C', '#BC6F45', '#D09C6A', '#E4C59E'],
    label: { formatter: '{b}\n{d}%', fontSize: 11, color: '#2C2418', lineHeight: 16 },
    labelLine: { lineStyle: { color: '#D9C5A7' } }
  }]
}))

const gradeChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c}件 ({d}%)' },
  series: [{
    type: 'pie',
    radius: ['42%', '70%'],
    padAngle: 2,
    itemStyle: { borderRadius: 6 },
    data: [
      { name: 'A 级', value: 98 },
      { name: 'B 级', value: 42 },
      { name: 'C 级', value: 16 }
    ],
    color: ['#5F7A61', '#D09C6A', '#9B3A1C'],
    label: { formatter: '{b}\n{d}%', fontSize: 11, color: '#2C2418', lineHeight: 16 },
    labelLine: { lineStyle: { color: '#D9C5A7' } }
  }]
}))

const statusChartOption = computed(() => ({
  tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c}件' },
  series: [{
    type: 'pie',
    radius: ['42%', '70%'],
    padAngle: 2,
    itemStyle: { borderRadius: 6 },
    data: [
      { name: '已完成', value: 16 },
      { name: '进行中', value: 5 },
      { name: '待处理', value: 3 }
    ],
    color: ['#5F7A61', '#C9A063', '#CF9F5A'],
    label: { formatter: '{b}\n{d}%', fontSize: 11, color: '#2C2418', lineHeight: 16 },
    labelLine: { lineStyle: { color: '#D9C5A7' } }
  }]
}))
</script>

<style scoped>
.data-dashboard {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 4px;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}
.header-title-wrap {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}
.seal-icon {
  width: 52px;
  height: 52px;
  flex-shrink: 0;
  margin-top: 4px;
}
.page-header h2 {
  font-size: 24px;
  color: var(--color-text);
  letter-spacing: 1px;
}
.header-subtitle {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
  font-family: 'Noto Sans SC', sans-serif;
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
  color: var(--color-green-mute);
  background: var(--bg-tag-green);
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 500;
}
.live-dot {
  width: 6px;
  height: 6px;
  background: var(--color-green-mute);
  border-radius: 50%;
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.fullscreen-btn { color: var(--color-text-secondary); }
.fullscreen-btn:hover { color: var(--color-primary); }
.kpi-row { margin-bottom: 20px; }
.charts-row { margin-bottom: 20px; }

.kpi-card {
  background: var(--bg-card-warm);
  border: 1px solid var(--color-border-card);
  border-radius: var(--card-radius);
  padding: 20px 24px;
  box-shadow: var(--shadow-card);
  backdrop-filter: blur(4px);
  transition: transform 0.25s, box-shadow 0.25s;
}
.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card-hover);
}
.kpi-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  letter-spacing: 0.5px;
}
.kpi-value-row {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin: 6px 0;
}
.kpi-value {
  font-size: 38px;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.1;
}
.kpi-unit {
  font-size: 13px;
  color: var(--color-text-secondary);
}
.kpi-sub {
  font-size: 12px;
  color: var(--color-text-muted);
}
</style>
