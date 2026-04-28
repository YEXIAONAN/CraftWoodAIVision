<template>
  <div class="inspection-result" v-loading="loading">
    <div class="page-header">
      <el-button text @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>返回
      </el-button>
      <h2>质检结果详情</h2>
    </div>

    <template v-if="item">
      <el-row :gutter="20">
        <el-col :span="14">
          <el-card shadow="never">
            <template #header>
              <span>检测图像对比</span>
            </template>
            <el-row :gutter="12">
              <el-col :span="12">
                <p class="img-label">原始图像</p>
                <el-image :src="item.image" fit="contain" style="width:100%;height:280px;border-radius:8px">
                  <template #error><div class="img-placeholder" /></template>
                </el-image>
              </el-col>
              <el-col :span="12">
                <p class="img-label">标注图像</p>
                <el-image :src="item.annotatedImage" fit="contain" style="width:100%;height:280px;border-radius:8px">
                  <template #error><div class="img-placeholder"><el-icon><Warning /></el-icon>标注预览</div></template>
                </el-image>
              </el-col>
            </el-row>
          </el-card>
        </el-col>

        <el-col :span="10">
          <el-card shadow="never">
            <template #header>检测信息</template>
            <el-descriptions :column="1" border size="small">
              <el-descriptions-item label="检测编号">{{ item.id }}</el-descriptions-item>
              <el-descriptions-item label="产品编号">{{ item.productId }}</el-descriptions-item>
              <el-descriptions-item label="产品名称">{{ item.productName }}</el-descriptions-item>
              <el-descriptions-item label="检测场景">{{ item.scene }}</el-descriptions-item>
              <el-descriptions-item label="检测人员">{{ item.inspector }}</el-descriptions-item>
              <el-descriptions-item label="检测日期">{{ item.date }}</el-descriptions-item>
              <el-descriptions-item label="风险等级">
                <StatusBadge :status="item.risk" :label="item.riskLabel" />
              </el-descriptions-item>
              <el-descriptions-item label="质检评分">
                <span :style="{ color: item.score >= 85 ? '#67c23a' : item.score >= 70 ? '#e6a23c' : '#f56c6c', fontWeight: 700 }">{{ item.score }}</span>
              </el-descriptions-item>
            </el-descriptions>
          </el-card>

          <el-card shadow="never" style="margin-top:16px">
            <template #header>缺陷清单</template>
            <el-table :data="item.defects" size="small" stripe>
              <el-table-column prop="type" label="类型" width="80" />
              <el-table-column label="置信度" width="90">
                <template #default="{ row }"> {{ (row.confidence * 100).toFixed(0) }}% </template>
              </el-table-column>
              <el-table-column prop="area" label="面积" width="70" />
            </el-table>
          </el-card>
        </el-col>
      </el-row>

      <el-card shadow="never" style="margin-top:16px">
        <template #header>处理建议</template>
        <div v-if="item.notes" class="notes-text">{{ item.notes }}</div>
        <div v-else class="notes-text">无明显异常，可正常流转。</div>
        <div style="margin-top:12px;display:flex;gap:8px">
          <el-button type="primary" @click="$router.push('/reports')">查看质检报告</el-button>
          <el-button @click="handleReview">确认复核</el-button>
        </div>
      </el-card>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { fetchInspectionById } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'

const route = useRoute()
const item = ref(null)
const loading = ref(false)

async function fetchData() {
  loading.value = true
  const res = await fetchInspectionById(route.params.id)
  item.value = res.data
  loading.value = false
}
function handleReview() {
  ElMessage.success('已标记为已复核')
}

onMounted(fetchData)
</script>

<style scoped>
.inspection-result { max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.page-header h2 { font-size: 20px; }
.img-label { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 8px; text-align: center; }
.img-placeholder { height: 280px; display: flex; align-items: center; justify-content: center; background: var(--color-bg); border-radius: 8px; color: var(--color-text-secondary); gap: 8px; }
.notes-text { font-size: 14px; color: var(--color-text); line-height: 1.6; }
</style>
