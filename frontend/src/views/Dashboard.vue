<template>
  <div class="dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h2>工作台</h2>
        <p class="header-subtitle">{{ greeting }}，{{ authStore.user?.name }} · 今日质检数据概览</p>
      </div>
      <el-button text class="fullscreen-btn" @click="toggleFullscreen">
        <el-icon :size="18"><FullScreen /></el-icon>
      </el-button>
    </div>

    <!-- Skeleton Loading -->
    <template v-if="loading">
      <el-row :gutter="20" class="kpi-row">
        <el-col :xs="12" :sm="6" v-for="i in 4" :key="i">
          <div class="skeleton skeleton-card" />
        </el-col>
      </el-row>
      <el-row :gutter="20" class="charts-row">
        <el-col :span="14"><div class="skeleton skeleton-chart" /></el-col>
        <el-col :span="10"><div class="skeleton skeleton-chart" /></el-col>
      </el-row>
      <div class="skeleton skeleton-row" v-for="i in 6" :key="'r'+i" />
    </template>

    <!-- Content -->
    <template v-else>
      <!-- KPI Row -->
      <el-row :gutter="20" class="kpi-row">
        <el-col :xs="12" :sm="6" v-for="stat in stats" :key="stat.label">
          <StatCard v-bind="stat" />
        </el-col>
      </el-row>

      <!-- Charts -->
      <el-row :gutter="20" class="charts-row">
        <el-col :span="14">
          <div class="rose-card">
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
      <div class="rose-card">
        <div class="card-header" style="justify-content: space-between;">
          <span>最近质检记录</span>
          <el-button text type="primary" size="small" @click="$router.push('/inspection')">
            查看全部
            <el-icon style="margin-left:4px"><ArrowRight /></el-icon>
          </el-button>
        </div>
        <div class="card-body">
          <el-table :data="recentInspections" stripe style="width: 100%" size="default">
            <el-table-column prop="id" label="编号" width="110" />
            <el-table-column prop="productName" label="产品名称" min-width="150" />
            <el-table-column prop="date" label="日期" width="110" />
            <el-table-column prop="scene" label="场景" width="100" />
            <el-table-column prop="inspector" label="检测人" width="100" />
            <el-table-column label="风险等级" width="110">
              <template #default="{ row }">
                <StatusBadge :status="row.risk" :label="row.riskLabel" />
              </template>
            </el-table-column>
            <el-table-column label="评分" width="130">
              <template #default="{ row }">
                <div class="score-cell">
                  <span class="score-num" :style="{ color: getScoreColor(row.score) }">{{ row.score }}</span>
                  <el-progress
                    :percentage="row.score"
                    :color="getScoreColor(row.score)"
                    :stroke-width="4"
                    :show-text="false"
                    style="flex:1;max-width:60px"
                  />
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { fetchDashboardStats, fetchInspections } from '@/api'
import type { Inspection, DefectDistItem } from '@/types'
import StatCard from '@/components/common/StatCard.vue'
import StatusBadge from '@/components/common/StatusBadge.vue'
import VChart from 'vue-echarts'

const authStore = useAuthStore()
const loading = ref(true)
const stats = ref<{ label: string; value: string | number; icon: string; color: string; unit: string; trend?: string; trendPercent?: string; subtext: string }[]>([])
const recentInspections = ref<Inspection[]>([])
const trendData = ref<{ dates: string[]; counts: number[]; passes: number[] }>({ dates: [], counts: [], passes: [] })
const defectData = ref<DefectDistItem[]>([])

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 9) return '早上好'
  if (h < 12) return '上午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

onMounted(async () => {
  try {
    const [statsRes, insRes] = await Promise.all([
      fetchDashboardStats(),
      fetchInspections(),
    ])
    const s = statsRes.data
    stats.value = [
      { label: '今日质检', value: s.todayInspections, icon: 'Camera', color: '#8B4513', unit: '件', subtext: '较昨日 +2' },
      { label: '异常产品', value: s.anomalyCount, icon: 'WarningFilled', color: '#C0392B', unit: '件', trend: 'down', trendPercent: '12.5', subtext: '较昨日减少' },
      { label: '质检通过率', value: s.passRate, icon: 'CircleCheckFilled', color: '#4A7C59', unit: '%', subtext: '高于目标值 3.5%' },
      { label: '产品总数', value: s.totalProducts, icon: 'GoodsFilled', color: '#B8944B', unit: '件', subtext: '累计建档' },
    ]
    recentInspections.value = insRes.data.list.slice(0, 6)
    trendData.value = {
      dates: s.weeklyTrend.map((t: { date: string }) => t.date),
      counts: s.weeklyTrend.map((t: { count: number }) => t.count),
      passes: s.weeklyTrend.map((t: { pass: number }) => t.pass),
    }
    defectData.value = s.defectDistribution
  } finally {
    loading.value = false
  }
})

function getScoreColor(score: number) {
  if (score >= 85) return '#4A7C59'
  if (score >= 70) return '#D4913E'
  return '#C0392B'
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
    backgroundColor: '#FFFFFF',
    borderColor: '#E8E0D5',
    borderWidth: 1,
    padding: [12, 16],
    textStyle: { color: '#1E1812', fontSize: 13 },
    formatter: (params: any[]) => {
      const date = params[0].axisValue
      let html = `<div style="font-weight:600;margin-bottom:6px;font-size:14px">${date}</div>`
      params.forEach((p: any) => {
        html += `<div style="display:flex;justify-content:space-between;gap:24px;margin-top:2px">
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
    icon: 'roundRect',
    itemWidth: 10,
    itemHeight: 4,
    textStyle: { color: '#6B5E4E', fontSize: 12 }
  },
  grid: { left: 48, right: 16, bottom: 44, top: 16 },
  xAxis: {
    type: 'category',
    data: trendData.value.dates,
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#9B8E7E', fontSize: 11 }
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#F0EBE2', type: 'dashed' } },
    axisLabel: { color: '#9B8E7E', fontSize: 11 }
  },
  series: [
    {
      name: '检测总数',
      type: 'bar',
      data: trendData.value.counts,
      barWidth: 20,
      itemStyle: {
        color: '#D4BD8C',
        borderRadius: [4, 4, 0, 0],
        emphasis: { color: '#B8944B' }
      },
      barGap: '30%'
    },
    {
      name: '合格数',
      type: 'line',
      data: trendData.value.passes,
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { color: '#8B4513', width: 2.5 },
      itemStyle: { color: '#8B4513', borderColor: '#FFFFFF', borderWidth: 3 },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(139, 69, 19, 0.10)' },
            { offset: 1, color: 'rgba(139, 69, 19, 0.01)' }
          ]
        }
      }
    }
  ]
}))

const defectOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    backgroundColor: '#FFFFFF',
    borderColor: '#E8E0D5',
    borderWidth: 1,
    padding: [12, 16],
    textStyle: { color: '#1E1812', fontSize: 13 },
    formatter: (params: any) => {
      return `<div style="font-weight:600;margin-bottom:4px">${params.name}</div>
        <div>数量: <b>${params.value}</b></div>
        <div>占比: <b>${params.percent}%</b></div>`
    }
  },
  series: [{
    type: 'pie',
    radius: ['48%', '74%'],
    center: ['50%', '48%'],
    padAngle: 2,
    itemStyle: { borderRadius: 8, borderColor: '#FFFFFF', borderWidth: 2 },
    label: {
      show: true,
      formatter: '{b}\n{d}%',
      fontSize: 11,
      color: '#1E1812',
      lineHeight: 16
    },
    labelLine: { lineStyle: { color: '#D4BD8C' } },
    data: defectData.value,
    color: ['#8B4513', '#A0724A', '#B8944B', '#C4A882', '#D4BD8C', '#6B5E4E', '#4A7C59']
  }]
}))
</script>

<style scoped>
.dashboard {
  max-width: 1320px;
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
  color: var(--color-text);
  letter-spacing: 0.04em;
}
.header-subtitle {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}
.fullscreen-btn {
  color: var(--color-text-muted);
  margin-top: 4px;
}
.fullscreen-btn:hover {
  color: var(--color-primary);
}

.kpi-row {
  margin-bottom: 20px;
}
.charts-row {
  margin-bottom: 20px;
}

.score-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}
.score-num {
  font-size: 14px;
  font-weight: 700;
  font-family: 'Inter', sans-serif;
  min-width: 36px;
}
</style>
