/** 账户相关服务。

提供收藏、浏览历史、帖子、草稿等API调用。
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
  timeout: 10000, // 10秒超时
})

/**
 * 从本地存储获取 Token。
 * 
 * @returns Token 字符串，如果不存在则返回 null。
 */
function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

/**
 * 设置请求拦截器，自动添加 Token。
 */
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

/** 帖子项接口（用于收藏、历史等列表）。 */
export interface PostItem {
  /** 帖子 ID。 */
  post_id: number
  /** 标题。 */
  title: string
  /** 合约代码。 */
  contract_code: string
  /** 止损价。 */
  stop_loss: number
  /** 现价（可选）。 */
  current_price?: number
  /** 简要建议。 */
  suggestion?: string
  /** 发布时间。 */
  publish_time: string
}

/**
 * 获取用户收藏列表。
 * 
 * @param page - 页码，从1开始。
 * @param pageSize - 每页数量。
 * @returns 收藏的帖子列表。
 */
export async function getCollections(
  page: number = 1,
  pageSize: number = 20
): Promise<{ posts: PostItem[] }> {
  const response = await apiClient.get('/api/v1/collections', {
    params: { page, page_size: pageSize }
  })
  return response.data
}

/**
 * 获取用户浏览历史。
 * 
 * @param page - 页码，从1开始。
 * @param pageSize - 每页数量。
 * @returns 浏览过的帖子列表。
 */
export async function getBrowseHistory(
  page: number = 1,
  pageSize: number = 20
): Promise<{ posts: PostItem[] }> {
  const response = await apiClient.get('/api/v1/browse-history', {
    params: { page, page_size: pageSize }
  })
  return response.data
}

/**
 * 获取用户发布的帖子。
 * 
 * @param page - 页码，从1开始。
 * @param pageSize - 每页数量。
 * @returns 帖子列表。
 */
export async function getUserPosts(
  page: number = 1,
  pageSize: number = 20
): Promise<any> {
  const response = await apiClient.get('/api/v1/posts', {
    params: { page, page_size: pageSize, author_id: 'current' }
  })
  return response.data
}

/**
 * 获取用户草稿列表。
 * 
 * @returns 草稿列表。
 */
export async function getDrafts(): Promise<{ drafts: any[] }> {
  const response = await apiClient.get('/api/v1/drafts')
  return response.data
}

