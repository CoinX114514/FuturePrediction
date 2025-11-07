/** 用户认证服务。

提供登录、注册、登出等认证相关的 API 调用。
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
})

/**
 * 从本地存储获取 Token。
 * 
 * @returns Token 字符串，如果不存在则返回 null。
 */
export function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

/**
 * 保存 Token 到本地存储。
 * 
 * @param token - Token 字符串。
 */
export function setToken(token: string): void {
  localStorage.setItem('auth_token', token)
}

/**
 * 从本地存储移除 Token。
 */
export function removeToken(): void {
  localStorage.removeItem('auth_token')
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

/**
 * 设置响应拦截器，处理认证错误。
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token 过期或无效，清除本地存储并跳转到登录页
      removeToken()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

/** 登录请求数据接口。 */
export interface LoginRequest {
  /** 手机号（与 email 二选一）。 */
  phone_number?: string
  /** 邮箱（与 phone_number 二选一）。 */
  email?: string
  /** 密码。 */
  password: string
}

/** 注册请求数据接口。 */
export interface RegisterRequest {
  /** 手机号。 */
  phone_number: string
  /** 密码。 */
  password: string
  /** 邮箱（可选）。 */
  email?: string
  /** 昵称（可选）。 */
  nickname?: string
}

/** 用户信息接口。 */
export interface UserInfo {
  /** 用户 ID。 */
  user_id: number
  /** 手机号。 */
  phone_number: string
  /** 邮箱。 */
  email?: string
  /** 昵称。 */
  nickname?: string
  /** 用户角色。 */
  user_role: number
  /** 头像 URL。 */
  avatar_url?: string
}

/**
 * 用户登录。
 * 
 * @param data - 登录请求数据。
 * @returns 包含用户信息和 Token 的响应数据。
 */
export async function login(data: LoginRequest) {
  const response = await apiClient.post('/api/v1/auth/login', data)
  const { token, user } = response.data
  
  if (token) {
    setToken(token)
  }
  
  return { user, token }
}

/**
 * 用户注册。
 * 
 * @param data - 注册请求数据。
 * @returns 包含用户信息和 Token 的响应数据。
 */
export async function register(data: RegisterRequest) {
  const response = await apiClient.post('/api/v1/auth/register', data)
  const { token, user } = response.data
  
  if (token) {
    setToken(token)
  }
  
  return { user, token }
}

/**
 * 用户登出。
 */
export async function logout() {
  try {
    await apiClient.post('/api/v1/auth/logout')
  } finally {
    removeToken()
  }
}

/**
 * 获取当前用户信息。
 * 
 * @returns 用户信息。
 */
export async function getCurrentUser(): Promise<UserInfo> {
  const response = await apiClient.get('/api/v1/auth/me')
  return response.data
}

/**
 * 检查用户是否已登录。
 * 
 * @returns 是否已登录。
 */
export function isAuthenticated(): boolean {
  return getToken() !== null
}

