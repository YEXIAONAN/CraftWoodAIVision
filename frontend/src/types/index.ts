// ---- Common ----
export interface ApiResponse<T = any> {
  code: number
  message?: string
  data: T
}

export interface PaginatedData<T> {
  list: T[]
  total: number
}

// ---- Auth ----
export interface UserInfo {
  id: number
  username: string
  name: string
  role: 'admin' | 'inspector' | 'sales' | 'consumer'
  avatar: string
}

export interface LoginResult {
  token: string
  user: UserInfo
}

// ---- Product ----
export interface Product {
  id: string
  name: string
  type: string
  dimensions: string
  material: string
  batch: string
  status: string
  inspector: string
  date: string
  image: string
  grade: string
}

export interface ProductCreate {
  name: string
  type: string
  material: string
  dimensions: string
  batch: string
  inspector: string
}

// ---- Inspection ----
export interface DefectItem {
  type: string
  confidence: number
  bbox: number[]
  area: number
}

export type RiskLevel = 'low' | 'medium' | 'high'
export type InspectionScene = '入库检测' | '仓储巡检' | '出库复检'

export interface Inspection {
  id: string
  productId: string
  productName: string
  date: string
  inspector: string
  scene: InspectionScene
  risk: RiskLevel
  riskLabel: string
  score: number
  defects: DefectItem[]
  image: string
  annotatedImage: string
  notes: string
  reviewed: boolean | number
}

export interface InspectionSubmit {
  scene: InspectionScene
  productId?: string
  image?: string
}

// ---- Warehouse ----
export type WarehouseAction = '入库' | '仓储巡检' | '出库复检' | '出库'

export interface WarehouseRecord {
  id: string
  productId: string
  productName: string
  action: WarehouseAction
  operator: string
  date: string
  notes: string
  status: string
}

// ---- Report ----
export interface Report {
  id: string
  productId: string
  productName: string
  date: string
  inspector: string
  conclusion: string
  risk: string
  score: number
}

// ---- After-Sales ----
export type AfterSalesType = '运输损坏' | '质量异议' | '表面瑕疵' | '尺寸不符'
export type AfterSalesStatus = '待处理' | '处理中' | '已完成' | '已关闭'

export interface AfterSalesRecord {
  id: string
  productId: string
  productName: string
  type: AfterSalesType
  description: string
  status: AfterSalesStatus
  customer: string
  date: string
  handler: string
}

// ---- Dashboard ----
export interface DefectDistItem {
  name: string
  value: number
}

export interface TrendItem {
  date: string
  count: number
  pass: number
}

export interface AfterSalesTypeItem {
  name: string
  value: number
}

export interface DashboardStats {
  todayInspections: number
  anomalyCount: number
  passRate: number
  totalProducts: number
  defectDistribution: DefectDistItem[]
  weeklyTrend: TrendItem[]
  afterSalesTypes: AfterSalesTypeItem[]
}

// ---- Trace ----
export interface TraceInspection {
  scene: string
  date: string
  result: string
  risk: string
}

export interface TraceData {
  productId: string
  name: string
  material: string
  dimensions: string
  batch: string
  grade: string
  inspections: TraceInspection[]
  reportUrl: string
  maintainTips: string
}
