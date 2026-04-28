<template>
  <div class="product-list">
    <div class="page-header">
      <h2>产品档案</h2>
      <el-button type="primary" @click="showForm = true">
        <el-icon><Plus /></el-icon>新建产品
      </el-button>
    </div>

    <!-- Filters -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filters">
        <el-form-item label="关键词">
          <el-input v-model="filters.keyword" placeholder="产品名称/编号" clearable @clear="fetchData" @keyup.enter="fetchData" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部" clearable @change="fetchData" style="width:140px">
            <el-option label="已入库" value="已入库" />
            <el-option label="仓储中" value="仓储中" />
            <el-option label="待出库" value="待出库" />
            <el-option label="已出库" value="已出库" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button @click="fetchData">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Table -->
    <el-card shadow="never">
      <el-table :data="products" stripe v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="编号" width="120" />
        <el-table-column prop="name" label="产品名称" min-width="150">
          <template #default="{ row }">
            <el-link type="primary" @click="$router.push(`/products/${row.id}`)">{{ row.name }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="material" label="材质" width="140" />
        <el-table-column prop="dimensions" label="规格" width="180" />
        <el-table-column prop="batch" label="批次" width="120" />
        <el-table-column prop="grade" label="等级" width="80" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.status" :label="row.status" />
          </template>
        </el-table-column>
        <el-table-column prop="inspector" label="负责人" width="100" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="$router.push(`/products/${row.id}`)">详情</el-button>
            <el-button text type="primary" size="small" @click="handleQR(row)">二维码</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-wrap">
        <el-pagination background layout="total, prev, pager, next" :total="total" />
      </div>
    </el-card>

    <!-- Create Dialog -->
    <el-dialog v-model="showForm" title="新建产品档案" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="产品名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="产品类型">
          <el-select v-model="form.type" style="width:100%">
            <el-option label="红木家具" value="红木家具" />
          </el-select>
        </el-form-item>
        <el-form-item label="材质">
          <el-input v-model="form.material" />
        </el-form-item>
        <el-form-item label="规格尺寸">
          <el-input v-model="form.dimensions" placeholder="如: 2200×850×450 mm" />
        </el-form-item>
        <el-form-item label="生产批次">
          <el-input v-model="form.batch" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="form.inspector" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确认创建</el-button>
      </template>
    </el-dialog>

    <!-- QR Dialog -->
    <el-dialog v-model="showQR" title="产品追溯码" width="360px">
      <div class="qr-display">
        <div class="qr-placeholder">
          <el-icon :size="48" color="#8B5E3C"><Goods /></el-icon>
          <p class="qr-product">{{ qrProduct?.name }}</p>
          <p class="qr-id">{{ qrProduct?.id }}</p>
          <div class="qr-code">
            <div class="qr-simulate">
              <div v-for="i in 20" :key="i" class="qr-row">
                <span v-for="j in 20" :key="j" class="qr-cell" :class="{ filled: (i * j + i + j) % 3 !== 0 }" />
              </div>
            </div>
          </div>
          <p class="qr-hint">扫码查看产品质检履历</p>
          <el-button type="primary" class="qr-btn">下载二维码</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchProducts, createProduct } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'

const products = ref([])
const total = ref(0)
const loading = ref(false)
const showForm = ref(false)
const showQR = ref(false)
const qrProduct = ref(null)

const filters = reactive({ keyword: '', status: '' })
const form = reactive({ name: '', type: '红木家具', material: '', dimensions: '', batch: '', inspector: '' })

async function fetchData() {
  loading.value = true
  const res = await fetchProducts(filters)
  products.value = res.data.list
  total.value = res.data.total
  loading.value = false
}
async function handleCreate() {
  await createProduct(form)
  ElMessage.success('创建成功')
  showForm.value = false
  fetchData()
}
function handleQR(row) {
  qrProduct.value = row
  showQR.value = true
}

onMounted(fetchData)
</script>

<style scoped>
.product-list { max-width: 1400px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }
.filter-card { margin-bottom: 16px; }
.pagination-wrap { display: flex; justify-content: center; margin-top: 20px; }
.qr-display { text-align: center; }
.qr-product { font-size: 16px; font-weight: 600; margin-top: 12px; }
.qr-id { font-size: 12px; color: var(--color-text-secondary); margin: 4px 0 16px; }
.qr-code { display: flex; justify-content: center; margin-bottom: 12px; }
.qr-simulate { width: 160px; height: 160px; display: grid; grid-template-rows: repeat(20, 1fr); gap: 1px; padding: 8px; background: var(--color-white); border: 2px solid var(--color-text); border-radius: 8px; }
.qr-row { display: grid; grid-template-columns: repeat(20, 1fr); gap: 1px; }
.qr-cell { aspect-ratio: 1; background: var(--color-white); }
.qr-cell.filled { background: var(--color-text); }
.qr-hint { font-size: 12px; color: var(--color-text-secondary); margin-bottom: 12px; }
.qr-btn { width: 100%; }
</style>
