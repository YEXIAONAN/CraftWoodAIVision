<template>
  <div class="report-detail" v-loading="loading">
    <div class="page-header">
      <el-button text @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>返回
      </el-button>
      <h2>质检报告</h2>
      <div class="header-actions">
        <el-button @click="handlePrint">打印</el-button>
        <el-button type="primary" @click="handleDownload">下载 PDF</el-button>
      </div>
    </div>

    <el-card shadow="never" v-if="report">
      <div class="report-title">
        <div class="report-stamp"><span>匠</span></div>
        <h2>产品质量检测报告</h2>
        <p>报告编号：{{ report.id }} | 生成日期：{{ report.date }}</p>
      </div>

      <el-divider />

      <el-descriptions :column="2" border>
        <el-descriptions-item label="产品编号" :span="1">{{ report.productId }}</el-descriptions-item>
        <el-descriptions-item label="产品名称" :span="1">{{ report.productName }}</el-descriptions-item>
        <el-descriptions-item label="检测人员">{{ report.inspector }}</el-descriptions-item>
        <el-descriptions-item label="检测日期">{{ report.date }}</el-descriptions-item>
        <el-descriptions-item label="质检结论">
          <span :style="{ color: report.conclusion === '合格' ? '#67c23a' : '#f56c6c', fontWeight: 600 }">{{ report.conclusion }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <StatusBadge :status="report.risk === '低风险' ? 'low' : report.risk === '中风险' ? 'medium' : 'high'" :label="report.risk" />
        </el-descriptions-item>
        <el-descriptions-item label="质检评分">
          <span :style="{ color: report.score >= 85 ? '#67c23a' : '#e6a23c', fontWeight: 700 }">{{ report.score }}</span>
        </el-descriptions-item>
      </el-descriptions>

      <el-divider />
      <h4 style="margin-bottom:12px">检测依据与说明</h4>
      <p class="report-note">
        本报告基于 AI 视觉检测模型对产品表面进行缺陷识别，结合人工复核后生成。检测结果仅反映本次送检产品表面质量状况，不作为产品整体质量承诺。
      </p>
      <p class="report-note" style="margin-top:8px">
        建议：产品出库前进行复检，运输过程中注意包装防护，售后问题请及时联系客服处理。
      </p>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { fetchReportById } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'

const route = useRoute()
const report = ref(null)
const loading = ref(false)

async function fetchData() {
  loading.value = true
  const res = await fetchReportById(route.params.id)
  report.value = res.data
  loading.value = false
}
function handlePrint() { window.print() }
function handleDownload() { ElMessage.success('报告下载中（演示功能）') }

onMounted(fetchData)
</script>

<style scoped>
.report-detail { max-width: 800px; margin: 0 auto; }
.page-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.page-header h2 { flex: 1; font-size: 20px; }
.header-actions { display: flex; gap: 8px; }
.report-title { text-align: center; padding: 20px 0; }
.report-stamp { width: 60px; height: 60px; border: 3px solid var(--color-primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; }
.report-stamp span { font-size: 28px; color: var(--color-primary); font-weight: bold; }
.report-title h2 { font-size: 22px; margin-bottom: 8px; }
.report-title p { font-size: 13px; color: var(--color-text-secondary); }
.report-note { font-size: 14px; color: var(--color-text-secondary); line-height: 1.8; text-indent: 2em; }
</style>
