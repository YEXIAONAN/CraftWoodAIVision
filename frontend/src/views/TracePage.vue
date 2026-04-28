<template>
  <div class="trace-page" v-loading="loading">
    <div class="trace-container" v-if="trace">
      <div class="trace-header">
        <div class="trace-brand">
          <div class="brand-icon">匠</div>
          <div>
            <h1>产品质量履历</h1>
            <p>扫码查询产品质检信息</p>
          </div>
        </div>
      </div>

      <el-card shadow="never" class="trace-card">
        <template #header>产品信息</template>
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="产品编号" :span="2">{{ trace.productId }}</el-descriptions-item>
          <el-descriptions-item label="产品名称">{{ trace.name }}</el-descriptions-item>
          <el-descriptions-item label="等级">{{ trace.grade }}</el-descriptions-item>
          <el-descriptions-item label="材质">{{ trace.material }}</el-descriptions-item>
          <el-descriptions-item label="规格">{{ trace.dimensions }}</el-descriptions-item>
          <el-descriptions-item label="生产批次" :span="2">{{ trace.batch }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card shadow="never" class="trace-card">
        <template #header>质检履历</template>
        <el-timeline>
          <el-timeline-item
            v-for="(ins, i) in trace.inspections"
            :key="i"
            :timestamp="ins.date"
            :color="ins.result === '合格' ? '#4A7C59' : '#D4913E'"
          >
            <p><strong>{{ ins.scene }}</strong> — {{ ins.result }}</p>
            <p style="font-size:12px;color:var(--color-text-muted);margin-top:2px">风险等级：{{ ins.risk }}</p>
          </el-timeline-item>
        </el-timeline>
      </el-card>

      <el-card shadow="never" class="trace-card">
        <template #header>养护建议</template>
        <p class="maintain-text">{{ trace.maintainTips }}</p>
      </el-card>

      <div class="trace-footer">
        <p>本报告由 AI 辅助生成，仅供参考</p>
        <p>© 匠木云检 · 智能质检与溯源平台</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchTraceData } from '@/api'

const route = useRoute()
const trace = ref(null)
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  const res = await fetchTraceData(route.params.productId)
  trace.value = res.data
  loading.value = false
})
</script>

<style scoped>
.trace-page {
  min-height: 100vh;
  background: var(--bg-main);
  display: flex;
  justify-content: center;
  padding: 40px 16px;
}
.trace-container { max-width: 640px; width: 100%; }
.trace-header { margin-bottom: 24px; }
.trace-brand { display: flex; align-items: center; gap: 16px; }
.brand-icon {
  width: 48px; height: 48px; background: var(--color-primary);
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: #FFFFFF; font-family: 'Noto Serif SC', serif; font-weight: 900;
}
.trace-brand h1 { font-size: 20px; color: var(--color-text); }
.trace-brand p { font-size: 13px; color: var(--color-text-muted); margin-top: 2px; }
.trace-card { margin-bottom: 16px; }
.maintain-text { font-size: 14px; line-height: 1.8; color: var(--color-text); }
.trace-footer { text-align: center; padding: 20px; font-size: 12px; color: var(--color-text-muted); }
.trace-footer p { margin-bottom: 4px; }
</style>
