<template>
  <el-tag
    :type="tagType"
    :class="['defect-tag', { highlighted }]"
    size="small"
  >
    {{ type }}
    <span v-if="confidence" class="confidence"> {{ (confidence * 100).toFixed(0) }}%</span>
  </el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  type?: string
  confidence?: number
  highlighted?: boolean
}>()

const defectTypeMap: Record<string, string> = {
  '裂纹': 'danger',
  '虫洞': 'danger',
  '划痕': 'warning',
  '磕碰': 'warning',
  '色差': 'info',
  '漆面异常': 'info',
  '接缝异常': 'warning',
}
const tagType = computed(() => defectTypeMap[props.type ?? ''] || 'info')
</script>

<style scoped>
.defect-tag {
  margin: 2px;
}
.defect-tag.highlighted {
  transform: scale(1.05);
}
.confidence {
  opacity: 0.8;
}
</style>
