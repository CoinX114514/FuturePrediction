import axios from 'axios'

/** API 基础 URL。 */
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000'

/** 创建 axios 实例。 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * 从本地存储获取 Token。
 * 
 * @returns Token 字符串，如果不存在则返回 null。
 */
function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

// 添加请求拦截器，自动添加 Token
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 移除开发模式下的 mock 逻辑，确保直接调用后端 API
// 如果需要 mock 数据，可以通过环境变量控制

/** 上传 CSV 文件。
 * 
 * @param file - 要上传的文件对象。
 * @returns Promise，解析为上传响应数据。
 */
export async function uploadFile(file: File) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

/** 执行趋势预测。
 * 
 * @param fileId - 已上传文件的 ID。
 * @param days - 预测未来天数，默认为 1。
 * @returns Promise，解析为预测结果数据。
 */
export async function predictTrend(fileId: string, days: number = 1) {
  const response = await apiClient.post('/api/predict', {
    file_id: fileId,
    days: days,
  })

  return response.data
}

/** 获取 CSV 格式要求。
 * 
 * @returns Promise，解析为格式要求数据。
 */
export async function getCSVFormat() {
  const response = await apiClient.get('/api/upload/validate')
  return response.data
}

/** 获取预测服务状态。
 * 
 * @returns Promise，解析为服务状态数据。
 */
export async function getPredictionStatus() {
  const response = await apiClient.get('/api/predict/status')
  return response.data
}

