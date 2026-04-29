<template>
  <div class="warehouse-page">
    <div class="page-header">
      <h2>出入库管理</h2>
      <div class="header-right">
        <el-input
          v-model="keyword"
          placeholder="搜索产品名称/编号"
          clearable
          style="width:220px"
          class="header-search"
          @clear="fetchData"
          @keyup.enter="fetchData"
        />
        <el-button type="primary" @click="openCreate">
          <el-icon><Plus /></el-icon>新建记录
        </el-button>
      </div>
    </div>

    <el-card shadow="never">
      <template #header>
        <el-radio-group v-model="filterAction" @change="fetchData" size="small">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="入库">入库</el-radio-button>
          <el-radio-button label="仓储巡检">仓储巡检</el-radio-button>
          <el-radio-button label="出库复检">出库复检</el-radio-button>
          <el-radio-button label="出库">出库</el-radio-button>
        </el-radio-group>
      </template>
      <el-table :data="records" stripe v-loading="loading">
        <el-table-column prop="id" label="记录编号" width="120" />
        <el-table-column prop="productId" label="产品编号" width="120" />
        <el-table-column prop="productName" label="产品名称" min-width="150" />
        <el-table-column prop="action" label="操作类型" width="100">
          <template #default="{ row }">
            <el-tag
              :type="row.action === '出库' ? 'warning' : row.action === '入库' ? 'success' : 'info'"
              size="small"
            >{{ row.action }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="notes" label="备注" min-width="180" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.status" :label="row.status" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="{ row }">
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

    <el-dialog v-model="showDialog" title="新建出入库记录" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品编号">
          <el-input v-model="form.productId" placeholder="如 PROD-0001" />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="form.productName" placeholder="可选" />
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select v-model="form.action" style="width:100%">
            <el-option label="入库" value="入库" />
            <el-option label="仓储巡检" value="仓储巡检" />
            <el-option label="出库复检" value="出库复检" />
            <el-option label="出库" value="出库" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.notes" type="textarea" :rows="3" placeholder="巡检记录、异常说明等" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleCreate">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fetchWarehouseRecords, createWarehouseRecord, deleteWarehouseRecord } from '@/api'
import type { WarehouseRecord } from '@/types'
import StatusBadge from '@/components/common/StatusBadge.vue'

const records = ref<WarehouseRecord[]>([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)
const showDialog = ref(false)
const filterAction = ref('')
const keyword = ref('')
const page = ref(1)
const pageSize = ref(10)
const form = reactive({ productId: '', productName: '', action: '入库', notes: '' })

async function fetchData() {
  loading.value = true
  try {
    const params: Record<string, string | number> = {
      page: page.value,
      page_size: pageSize.value,
    }
    if (filterAction.value) params.action = filterAction.value
    if (keyword.value) params.keyword = keyword.value
    const res = await fetchWarehouseRecords(params as any)
    records.value = res.data.list
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.productId = ''
  form.productName = ''
  form.action = '入库'
  form.notes = ''
  showDialog.value = true
}

async function handleCreate() {
  if (!form.productId) {
    ElMessage.warning('请输入产品编号')
    return
  }
  submitting.value = true
  try {
    await createWarehouseRecord({
      product_id: form.productId,
      product_name: form.productName,
      action: form.action,
      notes: form.notes,
    })
    ElMessage.success('记录创建成功')
    showDialog.value = false
    fetchData()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id: string) {
  try {
    await ElMessageBox.confirm(`确定删除记录 ${id}？`, '确认删除', { type: 'warning' })
    await deleteWarehouseRecord(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch { /* cancelled */ }
}

onMounted(fetchData)
</script>

<style scoped>
.warehouse-page { max-width: 1320px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.header-right { display: flex; gap: 12px; align-items: center; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 20px; }
</style>
