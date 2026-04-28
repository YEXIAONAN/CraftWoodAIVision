<template>
  <div class="dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-title-wrap">
        <img src="/src/assets/seal-stamp.svg" class="seal-icon" alt="" />
        <div>
          <h2>工作台</h2>
          <p class="header-subtitle">欢迎回来，{{ authStore.user?.name }} · 今日质检数据概览</p>
        </div>
      </div>
      <div class="header-actions">
        <el-button text class="fullscreen-btn" @click="toggleFullscreen">
          <el-icon><FullScreen /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- KPI Row -->
    <el-row :gutter="24" class="kpi-row">
      <el-col :xs="12" :sm="6" v-for="stat in stats" :key="stat.label">
        <StatCard v-bind="stat" />
      </el-col>
    </el-row>

    <!-- Charts -->
    <el-row :gutter="24" class="charts-row">
      <el-col :span="14">
        <div class="rose-card">
          <div class="card-accent" />
          <div class="card-header">
            <span>本周质检趋势</span>
          </div>
          <div class="card-body">
            <v-chart :option="trendOption" style="height: 320px" autoresize />
          </div>
        </div>
      </el-col>
      <el-col :span="10">
        <div class="rose-card">
          <div class="card-accent" />
          <div class="card-header">
            <span>缺陷类型分布</span>
          </div>
          <div class="card-body">
            <v-chart :option="defectOption" style="height: 320px" autoresize />
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- Recent Inspections -->
    <el-row :gutter="24">
      <el-col :span="24">
        <div class="rose-card">
          <div class="card-accent" />
          <div class="card-header" style="justify-content: space-between;">
            <span>最近质检记录</span>
            <el-button text type="primary" size="small" @click="$router.push('/inspection')">查看全部 →</el-button>
          </div>
          <div class="card-body">
            <el-table :data="recentInspections" stripe style="width: 100%" size="default">
              <el-table-column prop="id" label="编号" width="110" />
              <el-table-column prop="productName" label="产品名称" min-width="150" />
              <el-table-column prop="date" label="日期" width="120" />
              <el-table-column prop="scene" label="场景" width="100" />
              <el-table-column prop="inspector" label="检测人" width="100" />
              <el-table-column label="风险等级" width="110">
                <template #default="{ row }">
                  <StatusBadge :status="row.risk" :label="row.riskLabel" />
                </template>
              </el-table-column>
              <el-table-column label="评分" width="120">
                <template #default="{ row }">
                  <div class="score-bar">
                    <span class="score-num num" :style="{ color: getScoreColor(row.score) }">{{ row.score }}</span>
                    <el-progress
                      :percentage="row.score"
                      :color="getScoreColor(row.score)"
                      :stroke-width="4"
                      :show-text="false"
                      class="score-progress"
                    />
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { fetchDashboardStats, fetchInspections } from '@/api'
import StatCard from '@/components/common/StatCard.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart, GaugeChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { ElMessage } from 'element-plus'

use([CanvasRenderer, LineChart, BarChart, PieChart, GaugeChart, GridComponent, TooltipComponent, LegendComponent])

const authStore = useAuthStore()
const stats = ref([])
const recentInspections = ref([])
const trendData = ref({ dates: [], counts: [], passes: [] })
const defectData = ref([])

onMounted(async () => {
  const [statsRes, insRes] = await Promise.all([
    fetchDashboardStats(),
    fetchInspections()
  ])
  const s = statsRes.data
  stats.value = [
    { label: '今日质检', value: s.todayInspections, icon: 'Camera', color: '#9B3A1C', unit: '件', subtext: '较昨日 +2' },
    { label: '异常产品', value: s.anomalyCount, icon: 'WarningFilled', color: '#9B3A1C', unit: '件', trend: 'down', trendPercent: '12.5', subtext: '较昨日减少' },
    { label: '质检通过率', value: s.passRate, icon: 'CircleCheckFilled', color: '#5F7A61', unit: '%', subtext: '高于目标值 3.5%' },
    { label: '产品总数', value: s.totalProducts, icon: 'GoodsFilled', color: '#C9A063', unit: '件', subtext: '累计建档' },
  ]
  recentInspections.value = insRes.data.list.slice(0, 6)

  const trend = statsRes.data.weeklyTrend
  trendData.value = {
    dates: trend.map(t => t.date),
    counts: trend.map(t => t.count),
    passes: trend.map(t => t.pass)
  }
  defectData.value = statsRes.data.defectDistribution
})

function getScoreColor(score) {
  if (score >= 85) return '#5F7A61'
  if (score >= 70) return '#CF9F5A'
  return '#9B3A1C'
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

const trendOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255,245,235,0.95)',
    borderColor: '#D9C5A7',
    borderWidth: 1,
    textStyle: { color: '#2C2418', fontSize: 12 },
    formatter: (params) => {
      const date = params[0].axisValue
      let html = `<div style="font-weight:600;margin-bottom:4px">${date}</div>`
      params.forEach(p => {
        html += `<div style="display:flex;justify-content:space-between;gap:20px">
          <span>${p.marker} ${p.seriesName}</span>
          <b>${p.value}</b>
        </div>`
      })
      return html
    }
  },
  legend: {
    data: ['检测总数', '合格数'],
    bottom: 0,
    icon: 'circle',
    itemWidth: 8,
    itemHeight: 8,
    textStyle: { color: '#7E6B54', fontSize: 12 }
  },
  grid: { left: 50, right: 24, bottom: 40, top: 16 },
  xAxis: {
    type: 'category',
    data: trendData.value.dates,
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#7E6B54', fontSize: 11 },
    splitLine: { show: false }
  },
  yAxis: {
    type: 'value',
    splitLine: {
      lineStyle: { color: '#D9CBB8', type: 'dashed', width: 1 }
    },
    axisLabel: { color: '#7E6B54', fontSize: 11 }
  },
  series: [
    {
      name: '检测总数',
      type: 'bar',
      data: trendData.value.counts,
      barWidth: 24,
      itemStyle: {
        color: '#CDB89A',
        borderRadius: [4, 4, 0, 0],
        emphasis: { color: '#BC6F45' }
      }
    },
    {
      name: '合格数',
      type: 'line',
      data: trendData.value.passes,
      smooth: true,
      symbol: 'diamond',
      symbolSize: 10,
      lineStyle: { color: '#9B3A1C', width: 3 },
      itemStyle: { color: '#9B3A1C', borderColor: '#F7F4EB', borderWidth: 2 },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(155,58,28,0.15)' },
            { offset: 1, color: 'rgba(155,58,28,0.02)' }
          ]
        }
      }
    }
  ]
}))

const defectOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(255,245,235,0.95)',
    borderColor: '#D9C5A7',
    borderWidth: 1,
    textStyle: { color: '#2C2418', fontSize: 12 },
    formatter: (params) => {
      return `<div style="font-weight:500">${params.name}</div>
        <div style="margin-top:4px">数量: <b>${params.value}</b></div>
        <div>占比: <b>${params.percent}%</b></div>`
    }
  },
  series: [{
    type: 'pie',
    radius: ['45%', '72%'],
    center: ['50%', '50%'],
    avoidLabelOverlap: true,
    padAngle: 2,
    itemStyle: { borderRadius: 6 },
    label: {
      show: true,
      formatter: '{b}\n{d}%',
      fontSize: 11,
      color: '#2C2418',
      lineHeight: 16
    },
    labelLine: {
      lineStyle: { color: '#D9C5A7' }
    },
    data: defectData.value,
    color: ['#9B3A1C', '#BC6F45', '#D09C6A', '#E4C59E', '#CDB89A', '#A6937C', '#5F7A61']
  }]
}))
</script>

<style scoped>
.dashboard {
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
  font-weight: 400;
}
.fullscreen-btn {
  color: var(--color-text-secondary);
  font-size: 18px;
}
.fullscreen-btn:hover {
  color: var(--color-primary);
}
.kpi-row {
  margin-bottom: 24px;
}
.charts-row {
  margin-bottom: 24px;
}
.score-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}
.score-num {
  font-size: 14px;
  font-weight: 700;
  min-width: 32px;
}
.score-progress {
  flex: 1;
  max-width: 80px;
}
</style>
