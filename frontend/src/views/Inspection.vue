<template>
  <div class="inspection-page">
    <div class="page-header">
      <h2>AI 表面质检</h2>
    </div>

    <el-row :gutter="20">
      <el-col :span="10">
        <el-card shadow="never">
          <template #header><span class="card-title">上传检测图片</span></template>
          <div
            class="upload-area"
            :class="{ 'is-dragover': dragOver }"
            @dragover.prevent="dragOver = true"
            @dragleave.prevent="dragOver = false"
            @drop.prevent="handleDrop"
            @click="uploadRef?.click()"
          >
            <input ref="uploadRef" type="file" accept="image/*" hidden @change="handleFileChange" />
            <el-icon :size="40" color="#A0724A"><UploadFilled /></el-icon>
            <p class="upload-text">{{ preview ? '点击更换图片' : '拖拽或点击上传家具表面图片' }}</p>
            <p class="upload-hint">支持 JPG / PNG，单张不超过 10MB</p>
          </div>
          <div v-if="preview" class="preview-wrap">
            <el-image :src="preview" fit="contain" style="width:100%;height:240px;border-radius:10px" />
            <div class="preview-actions">
              <el-select v-model="scene" style="flex:1">
                <el-option label="入库检测" value="入库检测" />
                <el-option label="仓储巡检" value="仓储巡检" />
                <el-option label="出库复检" value="出库复检" />
              </el-select>
              <el-button type="primary" :loading="detecting" @click="startDetection">
                {{ detecting ? '检测中...' : '开始检测' }}
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="14">
        <el-card shadow="never">
          <template #header>
            <div class="card-header-row">
              <span class="card-title">检测结果</span>
              <span v-if="result" class="result-time">耗时 {{ result.duration }}ms</span>
            </div>
          </template>
          <div v-if="!result" class="empty-result">
            <el-icon :size="48" color="#C4A882"><Camera /></el-icon>
            <p>上传图片并点击"开始检测"以查看结果</p>
          </div>
          <div v-else>
            <div class="result-summary">
              <div class="summary-item">
                <span class="label">风险等级</span>
                <StatusBadge :status="result.risk" :label="result.riskLabel" />
              </div>
              <div class="summary-item">
                <span class="label">质检评分</span>
                <span :class="['score-big', result.score >= 85 ? 'text-green' : result.score >= 70 ? 'text-orange' : 'text-red']">
                  {{ result.score }}
                </span>
              </div>
              <div class="summary-item">
                <span class="label">缺陷数量</span>
                <span class="defect-count">{{ result.defects.length }}</span>
              </div>
            </div>
            <el-divider />
            <h4 class="section-title">缺陷明细</h4>
            <div class="defect-list">
              <el-tag
                v-for="(d, i) in result.defects"
                :key="i"
                closable
                :type="d.confidence > 0.85 ? 'danger' : 'warning'"
                class="defect-item"
                @close="result.defects.splice(i, 1)"
              >
                {{ d.type }} ({{ (d.confidence * 100).toFixed(0) }}%)
                <el-tooltip :content="`位置: [${d.bbox.join(', ')}]`">
                  <el-icon style="margin-left:4px;cursor:help"><InfoFilled /></el-icon>
                </el-tooltip>
              </el-tag>
            </div>
            <el-divider />
            <div class="result-actions">
              <el-button type="primary" @click="$router.push(`/inspection/result/${result.id}`)">查看详细报告</el-button>
              <el-button @click="resetUpload">重新检测</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { submitInspection } from '@/api'
import type { Inspection } from '@/types'
import StatusBadge from '@/components/common/StatusBadge.vue'

const uploadRef = ref<HTMLInputElement | null>(null)
const preview = ref('')
const dragOver = ref(false)
const detecting = ref(false)
const scene = ref<'入库检测' | '仓储巡检' | '出库复检'>('入库检测')
const result = ref<(Inspection & { duration: number }) | null>(null)

function handleFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) loadPreview(file)
}
function handleDrop(e: DragEvent) {
  dragOver.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) loadPreview(file)
}
function loadPreview(file: File) {
  if (!file.type.startsWith('image/')) {
    ElMessage.warning('请上传图片文件')
    return
  }
  preview.value = URL.createObjectURL(file)
  result.value = null
}
async function startDetection() {
  if (!preview.value) return
  detecting.value = true
  try {
    const res = await submitInspection({ scene: scene.value })
    result.value = { duration: Math.floor(800 + Math.random() * 1200), ...res.data }
    ElMessage.success('检测完成')
  } catch {
    ElMessage.error('检测失败')
  } finally {
    detecting.value = false
  }
}
function resetUpload() {
  preview.value = ''
  result.value = null
  if (uploadRef.value) uploadRef.value.value = ''
}
</script>

<style scoped>
.inspection-page { max-width: 1100px; margin: 0 auto; }
.page-header { margin-bottom: 20px; }
.page-header h2 { font-size: 22px; }

.card-title {
  font-family: 'Noto Serif SC', serif;
  font-weight: 600;
  font-size: 15px;
}
.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.upload-area {
  border: 2px dashed var(--color-border);
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s var(--ease-in-out);
  background: var(--bg-input);
}
.upload-area:hover,
.upload-area.is-dragover {
  border-color: var(--color-primary);
  background: var(--color-primary-bg);
}
.upload-text { margin-top: 12px; color: var(--color-text); font-size: 14px; }
.upload-hint { margin-top: 4px; font-size: 12px; color: var(--color-text-muted); }

.preview-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.empty-result {
  text-align: center;
  padding: 48px 20px;
  color: var(--color-text-muted);
}
.empty-result p { margin-top: 12px; }

.result-summary { display: flex; gap: 40px; }
.summary-item { display: flex; flex-direction: column; gap: 4px; }
.summary-item .label { font-size: 12px; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.04em; }

.score-big { font-size: 28px; font-weight: 800; font-family: 'Inter', sans-serif; }
.text-green { color: var(--color-green); }
.text-orange { color: var(--color-orange); }
.text-red { color: var(--color-red); }
.defect-count { font-size: 28px; font-weight: 800; font-family: 'Inter', sans-serif; color: var(--color-primary); }

.section-title { margin-bottom: 12px; font-size: 14px; }
.defect-list { display: flex; flex-wrap: wrap; gap: 6px; }
.defect-item { font-size: 13px; }

.result-time { font-size: 12px; color: var(--color-text-muted); }
.result-actions { display: flex; gap: 8px; }
</style>
