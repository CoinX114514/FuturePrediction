/** 帖子服务。

提供帖子相关的 API 调用。
*/

import axios from 'axios'

/** API 基础 URL。 */
// 在开发环境中，使用相对路径通过 vite 代理；生产环境使用环境变量或默认值
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 
  (import.meta.env.MODE === 'development' ? '/api' : 'http://localhost:8000/api')

/** 创建 axios 实例。 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 发布可能稍慢，放宽超时到 30 秒
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

/** 帖子信息接口。 */
export interface Post {
  /** 帖子 ID。 */
  post_id: number
  /** 标题。 */
  title: string
  /** 合约代码。 */
  contract_code: string
  /** 行权价（可选）。 */
  strike_price?: number
  /** 止损价。 */
  stop_loss: number
  /** 止盈价（可选）。 */
  take_profit?: number
  /** 现价（可选）。 */
  current_price?: number
  /** 交易方向：'buy' 或 'sell'（可选）。 */
  direction?: 'buy' | 'sell'
  /** 简要建议。 */
  suggestion?: string
  /** 作者 ID。 */
  author_id: number
  /** 作者昵称。 */
  author_nickname?: string
  /** 收藏数。 */
  collect_count: number
  /** 发布时间。 */
  publish_time: string
}

/** 帖子列表响应接口。 */
export interface PostsResponse {
  /** 帖子列表。 */
  posts: Post[]
  /** 总数。 */
  total: number
  /** 当前页码。 */
  page: number
  /** 每页数量。 */
  page_size: number
  /** 总页数。 */
  total_pages: number
}

/**
 * 获取帖子列表。
 * 
 * @param page - 页码，从1开始。
 * @param pageSize - 每页数量。
 * @param sectorId - 板块ID筛选（可选）。
 * @param search - 搜索关键词，用于搜索合约代码或标题（可选）。
 * @returns 帖子列表和分页信息。
 */
export async function getPosts(
  page: number = 1,
  pageSize: number = 20,
  sectorId?: number,
  search?: string
): Promise<PostsResponse> {
  const params: any = {
    page,
    page_size: pageSize,
  }
  
  if (sectorId) {
    params.sector_id = sectorId
  }
  
  if (search) {
    params.search = search
  }
  
  const response = await apiClient.get<PostsResponse>('/v1/posts', { params })
  return response.data
}

/**
 * 根据ID获取帖子详情。
 * 
 * @param postId - 帖子ID。
 * @returns 帖子详情。
 */
export async function getPostById(postId: number): Promise<any> {
  const response = await apiClient.get(`/v1/posts/${postId}`)
  return response.data
}

/** 创建帖子请求体。 */
export interface PostPayload {
  title: string
  contract_code: string
  stop_loss: number
  content: string
  take_profit?: number
  strike_price?: number
  current_price?: number
  direction?: 'buy' | 'sell'
  suggestion?: string
  k_line_image?: string
  sector_id?: number
}

/** 创建帖子（仅管理员）。 */
export async function createPost(data: PostPayload) {
  const response = await apiClient.post('/v1/posts', data)
  return response.data
}

/** 删除帖子（作者或管理员）。 */
export async function deletePost(postId: number) {
  const response = await apiClient.delete(`/v1/posts/${postId}`)
  return response.data
}

/** 更新帖子（作者或管理员）。 */
export async function updatePost(postId: number, data: Partial<PostPayload>) {
  const response = await apiClient.put(`/v1/posts/${postId}`, data)
  return response.data
}

