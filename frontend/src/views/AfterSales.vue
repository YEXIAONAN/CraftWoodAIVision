<template>
  <div class="after-sales-page">
    <div class="page-header">
      <h2>售后管理</h2>
      <div class="header-right">
        <el-input
          v-model="keyword"
          placeholder="搜索产品/客户"
          clearable
          style="width:220px"
          class="header-search"
          @clear="fetchData"
          @keyup.enter="fetchData"
        />
        <el-button type="primary" @click="openCreate">
          <el-icon><Plus /></el-icon>新建工单
        </el-button>
      </div>
    </div>

    <el-card shadow="never">
      <template #header>
        <el-radio-group v-model="filterStatus" @change="fetchData" size="small">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="待处理">待处理</el-radio-button>
          <el-radio-button label="处理中">处理中</el-radio-button>
          <el-radio-button label="已完成">已完成</el-radio-button>
          <el-radio-button label="已关闭">已关闭</el-radio-button>
        </el-radio-group>
      </template>
      <el-table :data="records" stripe v-loading="loading">
        <el-table-column prop="id" label="工单号" width="110" />
        <el-table-column prop="productName" label="产品" min-width="140" show-overflow-tooltip />
        <el-table-column prop="type" label="问题类型" width="120">
          <template #default="{ row }">
            <el-tag
              :type="row.type === '运输损坏' ? 'danger' : row.type === '质量异议' ? 'warning' : 'info'"
              size="small"
            >{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="问题描述" min-width="180" show-overflow-tooltip />
        <el-table-column prop="customer" label="客户" width="100" />
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="handler" label="处理人" width="100">
          <template #default="{ row }">
            {{ row.handler || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.status" :label="row.status" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === '待处理'" text type="primary" size="small" @click="handleProcess(row)">处理</el-button>
            <el-button v-if="row.status === '处理中'" text type="success" size="small" @click="handleComplete(row)">完成</el-button>
            <el-button v-if="row.status !== '已关闭'" text type="warning" size="small" @click="handleClose(row)">关闭</el-button>
            <el-button text type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-wrap">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="total"
          :page-size="pageSize"
          v-model:current-page="page"
          @current-change="fetchData"
        />
      </div>
    </el-card>

    <el-dialog v-model="showDialog" title="新建售后工单" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品编号">
          <el-input v-model="form.productId" placeholder="如 PROD-0001" />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="form.productName" placeholder="可选" />
        </el-form-item>
        <el-form-item label="问题类型">
          <el-select v-model="form.type" style="width:100%">
            <el-option label="运输损坏" value="运输损坏" />
            <el-option label="质量异议" value="质量异议" />
            <el-option label="表面瑕疵" value="表面瑕疵" />
            <el-option label="尺寸不符" value="尺寸不符" />
          </el-select>
        </el-form-item>
        <el-form-item label="问题描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请详细描述问题" />
        </el-form-item>
        <el-form-item label="客户姓名">
          <el-input v-model="form.customer" placeholder="客户称呼" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCreate">提交工单</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  fetchAfterSales,
  createAfterSales,
  processAfterSales,
  completeAfterSales,
  closeAfterSales,
  deleteAfterSales,
} from '@/api'
import type { AfterSalesRecord, AfterSalesType } from '@/types'
import StatusBadge from '@/components/common/StatusBadge.vue'

const records = ref<AfterSalesRecord[]>([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)
const showDialog = ref(false)
const filterStatus = ref('')
const keyword = ref('')
const page = ref(1)
const pageSize = ref(10)
const form = reactive({
  productId: '',
  productName: '',
  type: '运输损坏' as AfterSalesType,
  description: '',
  customer: '',
})

async function fetchData() {
  loading.value = true
  try {
    const params: Record<string, string | number> = {
      page: page.value,
      page_size: pageSize.value,
    }
    if (filterStatus.value) params.status = filterStatus.value
    if (keyword.value) params.keyword = keyword.value
    const res = await fetchAfterSales(params as any)
    records.value = res.data.list
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.productId = ''
  form.productName = ''
  form.type = '运输损坏'
  form.description = ''
  form.customer = ''
  showDialog.value = true
}

async function handleCreate() {
  if (!form.productId) {
    ElMessage.warning('请输入产品编号')
    return
  }
  if (!form.description) {
    ElMessage.warning('请输入问题描述')
    return
  }
  submitting.value = true
  try {
    await createAfterSales({
      product_id: form.productId,
      product_name: form.productName,
      type: form.type,
      description: form.description,
      customer: form.customer,
    })
    ElMessage.success('工单已提交')
    showDialog.value = false
    page.value = 1
    fetchData()
  } finally {
    submitting.value = false
  }
}

async function handleProcess(row: AfterSalesRecord) {
  try {
    await processAfterSales(row.id)
    ElMessage.success(`工单 ${row.id} 已开始处理`)
    fetchData()
  } catch { /* handled by interceptor */ }
}

async function handleComplete(row: AfterSalesRecord) {
  try {
    await completeAfterSales(row.id)
    ElMessage.success(`工单 ${row.id} 已完成`)
    fetchData()
  } catch { /* handled by interceptor */ }
}

async function handleClose(row: AfterSalesRecord) {
  try {
    await ElMessageBox.confirm(`确定关闭工单 ${row.id}？`, '确认关闭', { type: 'warning' })
    await closeAfterSales(row.id)
    ElMessage.success(`工单 ${row.id} 已关闭`)
    fetchData()
  } catch { /* cancelled */ }
}

async function handleDelete(id: string) {
  try {
    await ElMessageBox.confirm(`确定删除工单 ${id}？`, '确认删除', { type: 'warning' })
    await deleteAfterSales(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch { /* cancelled */ }
}

onMounted(fetchData)
</script>

<style scoped>
.after-sales-page { max-width: 1320px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.header-right { display: flex; gap: 12px; align-items: center; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 20px; }
</style>
