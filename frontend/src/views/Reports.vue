<template>
  <div class="reports-page">
    <div class="page-header">
      <h2>质检报告</h2>
      <div class="header-right">
        <el-input
          v-model="keyword"
          placeholder="搜索产品名称/编号"
          clearable
          style="width:240px"
          class="header-search"
          @clear="fetchData"
          @keyup.enter="fetchData"
        />
        <el-button type="primary" @click="openCreate">
          <el-icon><Plus /></el-icon>新建报告
        </el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="8" v-for="rpt in reports" :key="rpt.id" style="margin-bottom:20px">
        <el-card shadow="hover" class="report-card" @click="$router.push(`/reports/${rpt.id}`)">
          <div class="report-head">
            <el-icon :size="32" color="#8B4513"><Document /></el-icon>
            <div>
              <p class="report-name">{{ rpt.productName }}</p>
              <p class="report-id">{{ rpt.id }}</p>
            </div>
          </div>
          <el-divider />
          <div class="report-body">
            <div class="report-row">
              <span class="label">检测日期</span>
              <span>{{ rpt.date }}</span>
            </div>
            <div class="report-row">
              <span class="label">质检结论</span>
              <span :style="{ color: rpt.conclusion === '合格' ? '#4A7C59' : rpt.conclusion === '需复检' ? '#C0392B' : '#D4913E', fontWeight: 600 }">
                {{ rpt.conclusion }}
              </span>
            </div>
            <div class="report-row">
              <span class="label">风险等级</span>
              <StatusBadge
                :status="rpt.risk === '低风险' ? 'low' : rpt.risk === '中风险' ? 'medium' : 'high'"
                :label="rpt.risk"
              />
            </div>
            <div class="report-row">
              <span class="label">评分</span>
              <span class="fw-600">{{ rpt.score }}</span>
            </div>
          </div>
          <div class="report-footer">
            <el-button text type="primary" size="small" @click.stop="$router.push(`/reports/${rpt.id}`)">查看详情</el-button>
            <a :href="`/api/reports/${rpt.id}/download`" target="_blank" @click.stop>
              <el-button text size="small">下载</el-button>
            </a>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="pagination-wrap" v-if="total > pageSize">
      <el-pagination
        background
        layout="total, prev, pager, next"
        :total="total"
        :page-size="pageSize"
        v-model:current-page="page"
        @current-change="fetchData"
      />
    </div>

    <el-dialog v-model="showDialog" title="新建质检报告" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品编号">
          <el-input v-model="form.productId" placeholder="如 PROD-0001" />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="form.productName" placeholder="可选" />
        </el-form-item>
        <el-form-item label="质检结论">
          <el-select v-model="form.conclusion" style="width:100%">
            <el-option label="合格" value="合格" />
            <el-option label="条件合格" value="条件合格" />
            <el-option label="需复检" value="需复检" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="风险等级">
          <el-select v-model="form.risk" style="width:100%">
            <el-option label="低风险" value="低风险" />
            <el-option label="中风险" value="中风险" />
            <el-option label="高风险" value="高风险" />
          </el-select>
        </el-form-item>
        <el-form-item label="质检评分">
          <el-input-number v-model="form.score" :min="0" :max="100" :precision="1" style="width:100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCreate">生成报告</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchReports, createReport } from '@/api'
import type { Report } from '@/types'
import StatusBadge from '@/components/common/StatusBadge.vue'

const reports = ref<Report[]>([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)
const showDialog = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = ref(9)
const form = reactive({
  productId: '',
  productName: '',
  conclusion: '合格',
  risk: '低风险',
  score: 85.0,
})

async function fetchData() {
  loading.value = true
  try {
    const res = await fetchReports({
      keyword: keyword.value || undefined,
      page: page.value,
      page_size: pageSize.value,
    })
    reports.value = res.data.list
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.productId = ''
  form.productName = ''
  form.conclusion = '合格'
  form.risk = '低风险'
  form.score = 85.0
  showDialog.value = true
}

async function handleCreate() {
  if (!form.productId) {
    ElMessage.warning('请输入产品编号')
    return
  }
  submitting.value = true
  try {
    await createReport({
      product_id: form.productId,
      product_name: form.productName,
      conclusion: form.conclusion,
      risk: form.risk,
      score: form.score,
    })
    ElMessage.success('报告创建成功')
    showDialog.value = false
    page.value = 1
    fetchData()
  } finally {
    submitting.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.reports-page { max-width: 1320px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.header-right { display: flex; gap: 12px; align-items: center; }
.report-card { cursor: pointer; }
.report-head { display: flex; align-items: center; gap: 12px; }
.report-name { font-weight: 600; font-size: 15px; color: var(--color-text); }
.report-id { font-size: 12px; color: var(--color-text-muted); margin-top: 2px; }
.report-body { display: flex; flex-direction: column; gap: 8px; }
.report-row { display: flex; justify-content: space-between; font-size: 13px; }
.report-row .label { color: var(--color-text-muted); }
.report-footer {
  display: flex; justify-content: flex-end; gap: 8px;
  margin-top: 12px; padding-top: 12px;
  border-top: 1px solid var(--color-divider);
}
.pagination-wrap { display: flex; justify-content: center; margin-top: 20px; }
</style>
