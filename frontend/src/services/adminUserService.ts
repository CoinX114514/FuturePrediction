import axios from 'axios'

// 在开发环境中，强制使用相对路径通过 vite 代理；生产环境使用环境变量或默认值
// 注意：开发环境必须使用相对路径 '/api' 以通过 vite 代理，避免 CORS 和认证问题
const isDev = import.meta.env.MODE === 'development' || import.meta.env.DEV
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 
  (isDev ? '/api' : 'http://localhost:8000/api')

console.log('[adminUserService] 初始化 - MODE:', import.meta.env.MODE, 'DEV:', import.meta.env.DEV, 'API_BASE_URL:', API_BASE_URL)

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

apiClient.interceptors.request.use((config) => {
  const token = getToken()
  const url = config.url || ''
  const baseURL = config.baseURL || ''
  console.log('[adminUserService] 请求拦截器 - URL:', url, '完整URL:', baseURL + url)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('[adminUserService] 请求拦截器：已添加 Token，长度:', token.length)
  } else {
    console.warn('[adminUserService] 请求拦截器：未找到 Token')
  }
  return config
})

// 添加响应拦截器，处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[adminUserService] 响应错误:', error.response?.status, error.response?.data)
    if (error.response?.status === 401) {
      console.error('[adminUserService] 401 未授权错误，Token 可能无效或过期')
    }
    return Promise.reject(error)
  }
)

export interface AdminUser {
  user_id: number
  phone_number: string
  email?: string
  nickname?: string
  user_role: number
  is_active: boolean
  daily_prediction_limit?: number
  created_at?: string
}

export interface AdminUserPayload {
  phone_number?: string
  password?: string
  email?: string
  nickname?: string
  user_role?: number
  is_active?: boolean
  daily_prediction_limit?: number
}

export async function fetchUsers(page = 1, page_size = 20, keyword?: string) {
  console.log('[adminUserService] API_BASE_URL:', API_BASE_URL)
  console.log('[adminUserService] Token:', getToken() ? '存在' : '不存在')
  const res = await apiClient.get('/v1/admin/users', { params: { page, page_size, keyword } })
  return res.data as { users: AdminUser[]; total: number; page: number; page_size: number }
}

export async function createUser(payload: AdminUserPayload) {
  const res = await apiClient.post('/v1/admin/users', payload)
  return res.data as AdminUser
}

export async function updateUser(userId: number, payload: AdminUserPayload) {
  const res = await apiClient.put(`/v1/admin/users/${userId}`, payload)
  return res.data as AdminUser
}

export async function deleteUser(userId: number) {
  await apiClient.delete(`/v1/admin/users/${userId}`)
}

