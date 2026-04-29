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
  AfterSalesType,
  DashboardStats,
  TraceData,
} from '@/types'
import client from './client'

// ---- Auth ----
export async function loginApi(username: string, password: string): Promise<LoginResult> {
  const res = await client.post('/api/auth/login', { username, password })
  return res.data
}

export async function fetchCurrentUser() {
  const res = await client.get('/api/auth/me')
  return res.data
}

// ---- Dashboard ----
export async function fetchDashboardStats(): Promise<ApiResponse<DashboardStats>> {
  const res = await client.get('/api/dashboard/stats')
  return res.data
}

// ---- Products ----
export async function fetchProducts(params: {
  status?: string
  keyword?: string
  page?: number
  page_size?: number
} = {}): Promise<ApiResponse<PaginatedData<Product>>> {
  const res = await client.get('/api/products', { params })
  return res.data
}

export async function fetchProductById(id: string): Promise<ApiResponse<Product | undefined>> {
  const res = await client.get(`/api/products/${id}`)
  return res.data
}

export async function createProduct(data: ProductCreate): Promise<ApiResponse<Product>> {
  const res = await client.post('/api/products', data)
  return res.data
}

// ---- Inspections ----
export async function fetchInspections(params: {
  scene?: string
  page?: number
  page_size?: number
} = {}): Promise<ApiResponse<PaginatedData<Inspection>>> {
  const res = await client.get('/api/inspections', { params })
  return res.data
}

export async function fetchInspectionById(id: string): Promise<ApiResponse<Inspection | undefined>> {
  const res = await client.get(`/api/inspections/${id}`)
  return res.data
}

export async function submitInspection(data: InspectionSubmit): Promise<ApiResponse<Inspection>> {
  const res = await client.post('/api/inspections', data)
  return res.data
}

// ---- Warehouse ----
export async function fetchWarehouseRecords(params: {
  action?: WarehouseAction | ''
  keyword?: string
  page?: number
  page_size?: number
} = {}): Promise<ApiResponse<PaginatedData<WarehouseRecord>>> {
  const cleanParams: Record<string, string | number> = {}
  if (params.action) cleanParams.action = params.action
  if (params.keyword) cleanParams.keyword = params.keyword
  if (params.page) cleanParams.page = params.page
  if (params.page_size) cleanParams.page_size = params.page_size
  const res = await client.get('/api/warehouse', { params: cleanParams })
  return res.data
}

export async function createWarehouseRecord(data: {
  product_id: string
  product_name?: string
  action: string
  notes?: string
}): Promise<ApiResponse<WarehouseRecord>> {
  const res = await client.post('/api/warehouse', data)
  return res.data
}

export async function updateWarehouseRecord(id: string, data: Record<string, string>): Promise<ApiResponse<WarehouseRecord>> {
  const res = await client.put(`/api/warehouse/${id}`, data)
  return res.data
}

export async function deleteWarehouseRecord(id: string): Promise<ApiResponse<null>> {
  const res = await client.delete(`/api/warehouse/${id}`)
  return res.data
}

// ---- Reports ----
export async function fetchReports(params: {
  keyword?: string
  page?: number
  page_size?: number
} = {}): Promise<ApiResponse<PaginatedData<Report>>> {
  const cleanParams: Record<string, string | number> = {}
  if (params.keyword) cleanParams.keyword = params.keyword
  if (params.page) cleanParams.page = params.page
  if (params.page_size) cleanParams.page_size = params.page_size
  const res = await client.get('/api/reports', { params: cleanParams })
  return res.data
}

export async function fetchReportById(id: string): Promise<ApiResponse<Report & { product?: any; inspections?: any[] } | undefined>> {
  const res = await client.get(`/api/reports/${id}`)
  return res.data
}

export async function createReport(data: {
  product_id: string
  product_name?: string
  inspector?: string
  conclusion?: string
  risk?: string
  score?: number
}): Promise<ApiResponse<Report>> {
  const res = await client.post('/api/reports', data)
  return res.data
}

export async function updateReport(id: string, data: Record<string, any>): Promise<ApiResponse<Report>> {
  const res = await client.put(`/api/reports/${id}`, data)
  return res.data
}

export async function deleteReport(id: string): Promise<ApiResponse<null>> {
  const res = await client.delete(`/api/reports/${id}`)
  return res.data
}

export function getReportDownloadUrl(id: string): string {
  return `/api/reports/${id}/download`
}

// ---- After-Sales ----
export async function fetchAfterSales(params: {
  status?: AfterSalesStatus | ''
  keyword?: string
  page?: number
  page_size?: number
} = {}): Promise<ApiResponse<PaginatedData<AfterSalesRecord>>> {
  const cleanParams: Record<string, string | number> = {}
  if (params.status) cleanParams.status = params.status
  if (params.keyword) cleanParams.keyword = params.keyword
  if (params.page) cleanParams.page = params.page
  if (params.page_size) cleanParams.page_size = params.page_size
  const res = await client.get('/api/after-sales', { params: cleanParams })
  return res.data
}

export async function createAfterSales(data: {
  product_id: string
  product_name?: string
  type: AfterSalesType
  description: string
  customer: string
}): Promise<ApiResponse<AfterSalesRecord>> {
  const res = await client.post('/api/after-sales', data)
  return res.data
}

export async function updateAfterSales(id: string, data: Record<string, string>): Promise<ApiResponse<AfterSalesRecord>> {
  const res = await client.put(`/api/after-sales/${id}`, data)
  return res.data
}

export async function deleteAfterSales(id: string): Promise<ApiResponse<null>> {
  const res = await client.delete(`/api/after-sales/${id}`)
  return res.data
}

export async function processAfterSales(id: string): Promise<ApiResponse<AfterSalesRecord>> {
  const res = await client.put(`/api/after-sales/${id}/process`)
  return res.data
}

export async function completeAfterSales(id: string): Promise<ApiResponse<AfterSalesRecord>> {
  const res = await client.put(`/api/after-sales/${id}/complete`)
  return res.data
}

export async function closeAfterSales(id: string): Promise<ApiResponse<AfterSalesRecord>> {
  const res = await client.put(`/api/after-sales/${id}/close`)
  return res.data
}

// ---- Trace ----
export async function fetchTraceData(productId: string): Promise<ApiResponse<TraceData>> {
  const res = await client.get(`/api/trace/${productId}`)
  return res.data
}
