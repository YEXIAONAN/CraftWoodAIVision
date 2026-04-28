// Mock API service — simulates backend responses
// Replace each function with real axios calls when backend is ready

const delay = (ms = 300) => new Promise(r => setTimeout(r, ms))

import {
  mockProducts,
  mockInspections,
  mockWarehouseRecords,
  mockReports,
  mockAfterSales,
  mockDashboardStats,
  getMockTrace
} from '@/mock'

export async function fetchDashboardStats() {
  await delay()
  return { code: 200, data: mockDashboardStats }
}

export async function fetchProducts(params = {}) {
  await delay()
  let list = [...mockProducts]
  if (params.status) list = list.filter(p => p.status === params.status)
  if (params.keyword) list = list.filter(p => p.name.includes(params.keyword) || p.id.includes(params.keyword))
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchProductById(id) {
  await delay()
  const product = mockProducts.find(p => p.id === id)
  return { code: 200, data: product }
}

export async function createProduct(data) {
  await delay(500)
  return { code: 200, data: { id: 'PROD-' + String(Date.now()).slice(-4), ...data }, message: '创建成功' }
}

export async function fetchInspections(params = {}) {
  await delay()
  let list = [...mockInspections]
  if (params.scene) list = list.filter(i => i.scene === params.scene)
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchInspectionById(id) {
  await delay()
  const item = mockInspections.find(i => i.id === id)
  return { code: 200, data: item }
}

export async function submitInspection(data) {
  await delay(1500)
  const defects = [
    { type: '裂纹', confidence: 0.92, bbox: [120, 80, 65, 30], area: 180 },
    { type: '划痕', confidence: 0.85, bbox: [200, 150, 90, 15], area: 95 },
  ]
  return {
    code: 200,
    data: {
      id: 'INS-' + String(Date.now()).slice(-4),
      ...data,
      defects,
      risk: defects.length > 2 ? 'high' : 'low',
      riskLabel: defects.length > 2 ? '高风险' : '低风险',
      score: defects.length > 2 ? 72.5 : 91.3,
      date: new Date().toISOString().slice(0, 10)
    },
    message: '质检完成'
  }
}

export async function fetchWarehouseRecords(params = {}) {
  await delay()
  let list = [...mockWarehouseRecords]
  if (params.action) list = list.filter(r => r.action === params.action)
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchReports(params = {}) {
  await delay()
  let list = [...mockReports]
  if (params.keyword) list = list.filter(r => r.productName.includes(params.keyword))
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchReportById(id) {
  await delay()
  const report = mockReports.find(r => r.id === id)
  return { code: 200, data: report }
}

export async function fetchAfterSales(params = {}) {
  await delay()
  let list = [...mockAfterSales]
  if (params.status) list = list.filter(s => s.status === params.status)
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchTraceData(productId) {
  await delay()
  return { code: 200, data: getMockTrace(productId) }
}
