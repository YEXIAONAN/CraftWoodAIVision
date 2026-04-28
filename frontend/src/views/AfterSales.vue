<template>
  <div class="after-sales-page">
    <div class="page-header">
      <h2>售后管理</h2>
      <el-button type="primary" @click="showDialog = true">
        <el-icon><Plus /></el-icon>新建工单
      </el-button>
    </div>

    <el-card shadow="never">
      <template #header>
        <el-radio-group v-model="filterStatus" @change="fetchData" size="small">
          <el-radio-button label="">全部</el-radio-button>
          <el-radio-button label="待处理">待处理</el-radio-button>
          <el-radio-button label="处理中">处理中</el-radio-button>
          <el-radio-button label="已完成">已完成</el-radio-button>
        </el-radio-group>
      </template>
      <el-table :data="records" stripe v-loading="loading">
        <el-table-column prop="id" label="工单号" width="110" />
        <el-table-column prop="productName" label="产品" min-width="140" />
        <el-table-column prop="type" label="问题类型" width="120">
          <template #default="{ row }">
            <el-tag :type="row.type === '运输损坏' ? 'danger' : row.type === '质量异议' ? 'warning' : 'info'" size="small">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="问题描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="customer" label="客户" width="100" />
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="handler" label="处理人" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.status" :label="row.status" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === '待处理'" text type="primary" size="small" @click="handleProcess(row)">处理</el-button>
            <el-button v-else text size="small">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-wrap">
        <el-pagination background layout="total, prev, pager, next" :total="total" />
      </div>
    </el-card>

    <el-dialog v-model="showDialog" title="新建售后工单" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品编号">
          <el-input v-model="form.productId" />
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
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="客户姓名">
          <el-input v-model="form.customer" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">提交工单</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchAfterSales } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'

const records = ref([])
const total = ref(0)
const loading = ref(false)
const showDialog = ref(false)
const filterStatus = ref('')
const form = reactive({ productId: '', type: '运输损坏', description: '', customer: '' })

async function fetchData() {
  loading.value = true
  const params = filterStatus.value ? { status: filterStatus.value } : {}
  const res = await fetchAfterSales(params)
  records.value = res.data.list
  total.value = res.data.total
  loading.value = false
}
function handleCreate() {
  ElMessage.success('工单已提交')
  showDialog.value = false
  fetchData()
}
function handleProcess(row) {
  ElMessage.info(`开始处理工单 ${row.id}`)
}

onMounted(fetchData)
</script>

<style scoped>
.after-sales-page { max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 20px; }
</style>
