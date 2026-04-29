import type {
  Product,
  Inspection,
  WarehouseRecord,
  Report,
  AfterSalesRecord,
  DashboardStats,
  TraceData,
  UserInfo,
  LoginResult,
} from '@/types'

// ---- Auth ----
export function mockLogin(_username: string, _password: string): Promise<LoginResult> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        token: 'mock-jwt-token-' + Date.now(),
        user: {
          id: 1,
          username: 'admin',
          name: '张明远',
          role: 'admin',
          avatar: '',
        },
      })
    }, 500)
  })
}

export function mockCurrentUser(): UserInfo {
  return {
    id: 1,
    username: 'admin',
    name: '张明远',
    role: 'admin',
    avatar: '',
  }
}

// ---- Products ----
const productTypes = ['红酸枝木沙发', '鸡翅木餐桌', '大果紫檀书桌', '红木茶台', '花梨木衣柜', '刺猬紫檀床', '黑酸枝办公桌', '红木圈椅']
const statuses = ['已入库', '仓储中', '待出库', '已出库', '已归档']

function randomProducts(count = 18): Product[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `PROD-${String(i + 1).padStart(4, '0')}`,
    name: productTypes[i % productTypes.length],
    type: '红木家具',
    dimensions: `${180 + Math.floor(Math.random() * 120)}0 × ${80 + Math.floor(Math.random() * 60)}0 × ${40 + Math.floor(Math.random() * 40)}0 mm`,
    material: ['老挝大红酸枝', '缅甸鸡翅木', '大果紫檀', '东非黑黄檀'][i % 4],
    batch: `2025-BATCH-${Math.ceil((i + 1) / 4)}`,
    status: statuses[i % statuses.length],
    inspector: '张明远',
    date: `2026-0${1 + (i % 3)}-${String(10 + (i % 18)).padStart(2, '0')}`,
    image: `https://picsum.photos/seed/prod${i}/400/300`,
    grade: ['A级', 'B级', 'A级', 'A级', 'B级', 'C级'][i % 6],
  }))
}

export const mockProducts: Product[] = randomProducts(18)

// ---- Inspections ----
const defectTypes = ['裂纹', '虫洞', '划痕', '磕碰', '色差', '漆面异常', '接缝异常']
const riskLevels = ['low', 'medium', 'high'] as const
const riskLabels: Record<string, string> = { low: '低风险', medium: '中风险', high: '高风险' }

function randomInspections(count = 12): Inspection[] {
  return Array.from({ length: count }, (_, i) => {
    const defectCount = 1 + Math.floor(Math.random() * 5)
    const defects = Array.from({ length: defectCount }, () => ({
      type: defectTypes[Math.floor(Math.random() * defectTypes.length)],
      confidence: +(0.75 + Math.random() * 0.24).toFixed(2),
      bbox: [
        Math.floor(Math.random() * 300),
        Math.floor(Math.random() * 300),
        Math.floor(Math.random() * 100 + 30),
        Math.floor(Math.random() * 100 + 30),
      ],
      area: Math.floor(Math.random() * 500 + 10),
    }))
    const risk = riskLevels[Math.floor(Math.random() * riskLevels.length)]
    return {
      id: `INS-${String(i + 1).padStart(4, '0')}`,
      productId: `PROD-${String(Math.floor(Math.random() * 18) + 1).padStart(4, '0')}`,
      productName: productTypes[Math.floor(Math.random() * productTypes.length)],
      date: `2026-0${1 + (i % 3)}-${String(10 + (i % 18)).padStart(2, '0')}`,
      inspector: ['张明远', '李思琪', '王建国'][i % 3],
      scene: ['入库检测', '仓储巡检', '出库复检'][i % 3] as Inspection['scene'],
      risk,
      riskLabel: riskLabels[risk],
      score: +(60 + Math.random() * 40).toFixed(1),
      defects,
      image: `https://picsum.photos/seed/ins${i}/800/600`,
      annotatedImage: `https://picsum.photos/seed/ann${i}/800/600`,
      notes: defects.length > 3 ? '多处缺陷，建议人工复核' : '',
      reviewed: i % 3 === 0,
    }
  })
}

export const mockInspections: Inspection[] = randomInspections(12)

// ---- Warehouse Records ----
const warehouseActions: WarehouseRecord['action'][] = ['入库', '仓储巡检', '出库复检', '出库']

function randomWarehouseRecords(count = 10): WarehouseRecord[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `WH-${String(i + 1).padStart(4, '0')}`,
    productId: `PROD-${String(Math.floor(Math.random() * 18) + 1).padStart(4, '0')}`,
    productName: productTypes[Math.floor(Math.random() * productTypes.length)],
    action: warehouseActions[i % warehouseActions.length],
    operator: ['张明远', '李思琪', '刘强'][i % 3],
    date: `2026-0${1 + (i % 3)}-${String(10 + (i % 18)).padStart(2, '0')}`,
    notes: ['', '外观良好，无异常', '发现轻微划痕，已记录', '包装完整，准予出库'][i % 4],
    status: ['已完成', '待处理', '已完成', '已完成'][i % 4],
  }))
}

export const mockWarehouseRecords: WarehouseRecord[] = randomWarehouseRecords(10)

// ---- Reports ----
function randomReports(count = 8): Report[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `RPT-${String(i + 1).padStart(4, '0')}`,
    productId: `PROD-${String(Math.floor(Math.random() * 18) + 1).padStart(4, '0')}`,
    productName: productTypes[Math.floor(Math.random() * productTypes.length)],
    date: `2026-0${1 + (i % 3)}-${String(10 + (i % 18)).padStart(2, '0')}`,
    inspector: '张明远',
    conclusion: ['合格', '条件合格', '需复检', '合格'][i % 4],
    risk: riskLabels[riskLevels[i % 3]],
    score: +(70 + Math.random() * 30).toFixed(1),
  }))
}

export const mockReports: Report[] = randomReports(8)

// ---- After-Sales ----
const afterSalesTypes: AfterSalesRecord['type'][] = ['运输损坏', '质量异议', '表面瑕疵', '尺寸不符']
const afterSalesStatuses: AfterSalesRecord['status'][] = ['待处理', '处理中', '已完成', '已关闭']

function randomAfterSales(count = 6): AfterSalesRecord[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `AS-${String(i + 1).padStart(4, '0')}`,
    productId: `PROD-${String(Math.floor(Math.random() * 18) + 1).padStart(4, '0')}`,
    productName: productTypes[Math.floor(Math.random() * productTypes.length)],
    type: afterSalesTypes[i % afterSalesTypes.length],
    description: ['运输过程中出现磕碰', '客户反馈表面有细微划痕', '颜色与样品存在差异', '尺寸与订单不符'][i % 4],
    status: afterSalesStatuses[i % afterSalesStatuses.length],
    customer: '陈先生',
    date: `2026-0${1 + (i % 3)}-${String(10 + (i % 18)).padStart(2, '0')}`,
    handler: ['张明远', '李思琪', '', ''][i % 4],
  }))
}

export const mockAfterSales: AfterSalesRecord[] = randomAfterSales(6)

// ---- Dashboard Stats ----
export const mockDashboardStats: DashboardStats = {
  todayInspections: 24,
  anomalyCount: 3,
  passRate: 87.5,
  totalProducts: 156,
  defectDistribution: [
    { name: '裂纹', value: 35 },
    { name: '虫洞', value: 18 },
    { name: '划痕', value: 42 },
    { name: '磕碰', value: 28 },
    { name: '色差', value: 15 },
    { name: '漆面异常', value: 22 },
    { name: '接缝异常', value: 10 },
  ],
  weeklyTrend: [
    { date: '04-21', count: 18, pass: 16 },
    { date: '04-22', count: 22, pass: 19 },
    { date: '04-23', count: 15, pass: 13 },
    { date: '04-24', count: 28, pass: 24 },
    { date: '04-25', count: 20, pass: 18 },
    { date: '04-26', count: 12, pass: 11 },
    { date: '04-27', count: 24, pass: 21 },
  ],
  afterSalesTypes: [
    { name: '运输损坏', value: 5 },
    { name: '质量异议', value: 3 },
    { name: '表面瑕疵', value: 8 },
    { name: '尺寸不符', value: 2 },
  ],
}

// ---- Trace Record ----
export function getMockTrace(productId: string): TraceData {
  return {
    productId,
    name: '红酸枝木沙发',
    material: '老挝大红酸枝',
    dimensions: '2200 × 850 × 450 mm',
    batch: '2025-BATCH-2',
    grade: 'A级',
    inspections: [
      { scene: '入库检测', date: '2025-12-10', result: '合格', risk: '低风险' },
      { scene: '仓储巡检', date: '2026-01-15', result: '合格', risk: '低风险' },
      { scene: '出库复检', date: '2026-02-01', result: '合格', risk: '低风险' },
    ],
    reportUrl: '#',
    maintainTips: '避免阳光直射，保持室内湿度40%-60%，定期用软布清洁。',
  }
}
