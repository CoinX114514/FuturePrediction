/** 草稿服务。
 *
 * 提供草稿的增删改查 API 调用。
 */

import axios from 'axios'

/** API 基础 URL。 */
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000'

/** 创建 axios 实例。 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

/** 从本地存储获取 Token。 */
function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

/** 请求拦截器：自动添加 Token。 */
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/** 草稿列表项。 */
export interface DraftSummary {
  draft_id: number
  title?: string | null
  contract_code?: string | null
  update_time: string
}

/** 草稿详情。 */
export interface DraftDetail extends DraftSummary {
  stop_loss?: number | null
  take_profit?: number | null
  content?: string | null
  k_line_image?: string | null
}

/** 草稿请求体。 */
export interface DraftPayload {
  title?: string
  contract_code?: string
  stop_loss?: number
  take_profit?: number
  content?: string
  k_line_image?: string
}

/** 获取草稿列表。 */
export async function getDrafts(): Promise<DraftSummary[]> {
  const response = await apiClient.get('/api/v1/drafts')
  return response.data.drafts || []
}

/** 获取草稿详情。 */
export async function getDraftById(draftId: number): Promise<DraftDetail> {
  const response = await apiClient.get(`/api/v1/drafts/${draftId}`)
  return response.data
}

/** 创建草稿。 */
export async function createDraft(payload: DraftPayload): Promise<DraftDetail> {
  const response = await apiClient.post('/api/v1/drafts', payload)
  const draftId = response.data.draft_id
  return getDraftById(draftId)
}

/** 更新草稿。 */
export async function updateDraft(draftId: number, payload: DraftPayload): Promise<DraftDetail> {
  await apiClient.put(`/api/v1/drafts/${draftId}`, payload)
  return getDraftById(draftId)
}

/** 删除草稿。 */
export async function deleteDraft(draftId: number): Promise<void> {
  await apiClient.delete(`/api/v1/drafts/${draftId}`)
}

