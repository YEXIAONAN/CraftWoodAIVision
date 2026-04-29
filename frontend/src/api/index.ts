import type {
  ApiResponse,
  PaginatedData,
  LoginResult,
  Product,
  ProductCreate,
  Inspection,
  InspectionSubmit,
  WarehouseRecord,
  WarehouseAction,
  Report,
  AfterSalesRecord,
  AfterSalesStatus,
  DashboardStats,
  TraceData,
} from '@/types'

const delay = (ms = 300) => new Promise<void>(r => setTimeout(r, ms))

import {
  mockProducts,
  mockInspections,
  mockWarehouseRecords,
  mockReports,
  mockAfterSales,
  mockDashboardStats,
  getMockTrace,
} from '@/mock'

export async function fetchDashboardStats(): Promise<ApiResponse<DashboardStats>> {
  await delay()
  return { code: 200, data: mockDashboardStats }
}

export async function fetchProducts(params: {
  status?: string
  keyword?: string
} = {}): Promise<ApiResponse<PaginatedData<Product>>> {
  await delay()
  let list = [...mockProducts]
  const { status, keyword } = params
  if (status) list = list.filter(p => p.status === status)
  if (keyword) list = list.filter(p => p.name.includes(keyword) || p.id.includes(keyword))
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchProductById(id: string): Promise<ApiResponse<Product | undefined>> {
  await delay()
  const product = mockProducts.find(p => p.id === id)
  return { code: 200, data: product }
}

export async function createProduct(data: ProductCreate): Promise<ApiResponse<Product>> {
  await delay(500)
  return { code: 200, data: { id: 'PROD-' + String(Date.now()).slice(-4), ...data } as Product, message: '创建成功' }
}

export async function fetchInspections(params: {
  scene?: string
} = {}): Promise<ApiResponse<PaginatedData<Inspection>>> {
  await delay()
  let list = [...mockInspections]
  if (params.scene) list = list.filter(i => i.scene === params.scene)
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchInspectionById(id: string): Promise<ApiResponse<Inspection | undefined>> {
  await delay()
  const item = mockInspections.find(i => i.id === id)
  return { code: 200, data: item }
}

export async function submitInspection(data: InspectionSubmit): Promise<ApiResponse<Inspection>> {
  await delay(1500)
  const defects = [
    { type: '裂纹', confidence: 0.92, bbox: [120, 80, 65, 30], area: 180 },
    { type: '划痕', confidence: 0.85, bbox: [200, 150, 90, 15], area: 95 },
  ]
  return {
    code: 200,
    data: {
      id: 'INS-' + String(Date.now()).slice(-4),
      productId: data.productId ?? '',
      productName: '',
      date: new Date().toISOString().slice(0, 10),
      inspector: '',
      scene: data.scene,
      defects,
      risk: 'low',
      riskLabel: '低风险',
      score: 91.3,
      image: data.image ?? '',
      annotatedImage: '',
      notes: '',
      reviewed: false,
    },
    message: '质检完成',
  }
}

export async function fetchWarehouseRecords(params: {
  action?: WarehouseAction
} = {}): Promise<ApiResponse<PaginatedData<WarehouseRecord>>> {
  await delay()
  let list = [...mockWarehouseRecords]
  if (params.action) list = list.filter(r => r.action === params.action)
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchReports(params: {
  keyword?: string
} = {}): Promise<ApiResponse<PaginatedData<Report>>> {
  await delay()
  let list = [...mockReports]
  const { keyword } = params
  if (keyword) list = list.filter(r => r.productName.includes(keyword))
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchReportById(id: string): Promise<ApiResponse<Report | undefined>> {
  await delay()
  const report = mockReports.find(r => r.id === id)
  return { code: 200, data: report }
}

export async function fetchAfterSales(params: {
  status?: AfterSalesStatus
} = {}): Promise<ApiResponse<PaginatedData<AfterSalesRecord>>> {
  await delay()
  let list = [...mockAfterSales]
  if (params.status) list = list.filter(s => s.status === params.status)
  return { code: 200, data: { list, total: list.length } }
}

export async function fetchTraceData(productId: string): Promise<ApiResponse<TraceData>> {
  await delay()
  return { code: 200, data: getMockTrace(productId) }
}
