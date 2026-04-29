<template>
  <div class="product-detail" v-loading="loading">
    <div class="page-header">
      <el-button text @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>返回
      </el-button>
      <h2>{{ product?.name || '产品详情' }}</h2>
    </div>

    <el-row :gutter="20" v-if="product">
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>产品图片</template>
          <div class="product-image">
            <el-image :src="product.image" fit="cover" style="width:100%;height:220px;border-radius:10px">
              <template #error>
                <div class="image-placeholder">
                  <el-icon :size="32" color="#C4A882"><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>基本信息</template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="编号">{{ product.id }}</el-descriptions-item>
            <el-descriptions-item label="名称">{{ product.name }}</el-descriptions-item>
            <el-descriptions-item label="类型">{{ product.type }}</el-descriptions-item>
            <el-descriptions-item label="材质">{{ product.material }}</el-descriptions-item>
            <el-descriptions-item label="规格">{{ product.dimensions }}</el-descriptions-item>
            <el-descriptions-item label="批次">{{ product.batch }}</el-descriptions-item>
            <el-descriptions-item label="等级">{{ product.grade }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <StatusBadge :status="product.status" :label="product.status" />
            </el-descriptions-item>
            <el-descriptions-item label="负责人">{{ product.inspector }}</el-descriptions-item>
            <el-descriptions-item label="建档日期">{{ product.date }}</el-descriptions-item>
          </el-descriptions>
          <div class="actions">
            <el-button type="primary" @click="$router.push(`/inspection?productId=${product.id}`)">发起质检</el-button>
            <el-button @click="$router.push(`/reports?productId=${product.id}`)">质检报告</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchProductById } from '@/api'
import type { Product } from '@/types'
import StatusBadge from '@/components/common/StatusBadge.vue'

const route = useRoute()
const product = ref<Product | null>(null)
const loading = ref(false)

async function fetchData() {
  loading.value = true
  const res = await fetchProductById(route.params.id as string)
  product.value = res.data ?? null
  loading.value = false
}

onMounted(fetchData)
</script>

<style scoped>
.product-detail { max-width: 1100px; margin: 0 auto; }
.page-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.page-header h2 { font-size: 20px; }
.product-image { display: flex; justify-content: center; }
.image-placeholder {
  height: 220px; display: flex; align-items: center; justify-content: center;
  background: var(--bg-input); border-radius: 10px;
}
.actions { margin-top: 16px; display: flex; gap: 8px; }
</style>
