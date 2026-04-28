<template>
  <div class="reports-page">
    <div class="page-header">
      <h2>质检报告</h2>
      <el-input v-model="keyword" placeholder="搜索产品名称" clearable style="width:240px" @clear="fetchData" @keyup.enter="fetchData" />
    </div>

    <el-row :gutter="20">
      <el-col :span="8" v-for="rpt in reports" :key="rpt.id" style="margin-bottom:20px">
        <el-card shadow="hover" class="report-card" @click="$router.push(`/reports/${rpt.id}`)">
          <div class="report-header">
            <el-icon :size="32" color="#8B5E3C"><Document /></el-icon>
            <div class="report-meta">
              <p class="report-name">{{ rpt.productName }}</p>
              <p class="report-id">{{ rpt.id }}</p>
            </div>
          </div>
          <el-divider />
          <div class="report-body">
            <div class="report-info">
              <span class="label">检测日期</span>
              <span>{{ rpt.date }}</span>
            </div>
            <div class="report-info">
              <span class="label">质检结论</span>
              <span :style="{ color: rpt.conclusion === '合格' ? '#67c23a' : rpt.conclusion === '需复检' ? '#f56c6c' : '#e6a23c', fontWeight: 600 }">{{ rpt.conclusion }}</span>
            </div>
            <div class="report-info">
              <span class="label">风险等级</span>
              <StatusBadge :status="rpt.risk === '低风险' ? 'low' : rpt.risk === '中风险' ? 'medium' : 'high'" :label="rpt.risk" />
            </div>
            <div class="report-info">
              <span class="label">评分</span>
              <span>{{ rpt.score }}</span>
            </div>
          </div>
          <div class="report-footer">
            <el-button text type="primary" size="small" @click.stop="$router.push(`/reports/${rpt.id}`)">查看详情</el-button>
            <el-button text size="small" @click.stop>下载</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchReports } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'

const reports = ref([])
const keyword = ref('')

async function fetchData() {
  const res = await fetchReports({ keyword: keyword.value })
  reports.value = res.data.list
}

onMounted(fetchData)
</script>

<style scoped>
.reports-page { max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.report-card { cursor: pointer; border: 1px solid var(--color-border); transition: transform 0.2s; }
.report-card:hover { transform: translateY(-4px); }
.report-header { display: flex; align-items: center; gap: 12px; }
.report-name { font-weight: 600; font-size: 15px; }
.report-id { font-size: 12px; color: var(--color-text-secondary); margin-top: 2px; }
.report-body { display: flex; flex-direction: column; gap: 8px; }
.report-info { display: flex; justify-content: space-between; font-size: 13px; }
.report-info .label { color: var(--color-text-secondary); }
.report-footer { display: flex; justify-content: flex-end; gap: 8px; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--color-border-light); }
</style>
