/** 注册页面组件。

提供用户注册功能，支持手机号和邮箱注册。
*/

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../services/authService'

/** 注册表单数据接口。 */
interface RegisterFormData {
  /** 手机号。 */
  phoneNumber: string
  /** 邮箱（可选）。 */
  email: string
  /** 密码。 */
  password: string
  /** 确认密码。 */
  confirmPassword: string
  /** 昵称（可选）。 */
  nickname: string
}

/**
 * 注册页面组件。
 * 
 * @returns JSX 元素。
 */
export default function Register() {
  /** 导航钩子。 */
  const navigate = useNavigate()
  
  /** 注册表单数据。 */
  const [formData, setFormData] = useState<RegisterFormData>({
    phoneNumber: '',
    email: '',
    password: '',
    confirmPassword: '',
    nickname: '',
  })
  
  /** 加载状态。 */
  const [loading, setLoading] = useState(false)
  
  /** 错误信息。 */
  const [error, setError] = useState<string | null>(null)

  /**
   * 处理表单输入变化。
   * 
   * @param e - 输入事件。
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }))
    setError(null)
  }

  /**
   * 验证表单数据。
   * 
   * @returns 是否验证通过。
   */
  const validateForm = (): boolean => {
    if (formData.phoneNumber.length !== 11 || !/^\d+$/.test(formData.phoneNumber)) {
      setError('手机号必须是11位数字')
      return false
    }

    if (formData.password.length < 6) {
      setError('密码长度至少为6位')
      return false
    }

    if (formData.password !== formData.confirmPassword) {
      setError('两次输入的密码不一致')
      return false
    }

    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      setError('邮箱格式不正确')
      return false
    }

    return true
  }

  /**
   * 处理表单提交。
   * 
   * @param e - 表单提交事件。
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // 前端验证
    if (!validateForm()) {
      return
    }

    setLoading(true)

    try {
      const registerData = {
        phone_number: formData.phoneNumber,
        password: formData.password,
        email: formData.email || undefined,
        nickname: formData.nickname || undefined,
      }

      // 调用注册 API（register 函数会自动保存 token）
      const response = await register(registerData)
      
      // 注册成功，token 已自动保存，直接跳转到首页
      if (response.token) {
        // 延迟一小段时间让用户看到成功状态
        setTimeout(() => {
          navigate('/dashboard')
        }, 500)
      } else {
        // 如果没有 token，跳转到登录页
        navigate('/login', { 
          state: { message: '注册成功，请登录' } 
        })
      }
    } catch (err: any) {
      // 处理各种错误情况
      let errorMessage = '注册失败，请重试'
      
      if (err.response) {
        // 服务器返回的错误
        const detail = err.response.data?.detail
        if (detail) {
          errorMessage = detail
        } else if (err.response.status === 400) {
          errorMessage = '请求数据格式错误，请检查输入'
        } else if (err.response.status === 409) {
          errorMessage = '手机号或邮箱已被注册'
        } else if (err.response.status >= 500) {
          errorMessage = '服务器错误，请稍后重试'
        }
      } else if (err.request) {
        // 请求发送但无响应
        errorMessage = '网络错误，请检查网络连接'
      } else if (err.message) {
        // 其他错误
        errorMessage = err.message
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4 py-8">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
        {/* 标题 */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">创建账户</h1>
          <p className="text-gray-600">注册新账户以开始使用</p>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* 注册表单 */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 手机号输入 */}
          <div>
            <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-700 mb-2">
              手机号 <span className="text-red-500">*</span>
            </label>
            <input
              type="tel"
              id="phoneNumber"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange}
              required
              placeholder="请输入11位手机号"
              maxLength={11}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 邮箱输入（可选） */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              邮箱地址 <span className="text-gray-400 text-xs">(可选)</span>
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="请输入邮箱地址"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 昵称输入（可选） */}
          <div>
            <label htmlFor="nickname" className="block text-sm font-medium text-gray-700 mb-2">
              昵称 <span className="text-gray-400 text-xs">(可选)</span>
            </label>
            <input
              type="text"
              id="nickname"
              name="nickname"
              value={formData.nickname}
              onChange={handleChange}
              placeholder="请输入昵称"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 密码输入 */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              密码 <span className="text-red-500">*</span>
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="至少6位字符"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 确认密码输入 */}
          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
              确认密码 <span className="text-red-500">*</span>
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              placeholder="请再次输入密码"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 提交按钮 */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors mt-6"
          >
            {loading ? '注册中...' : '注册'}
          </button>
        </form>

        {/* 登录链接 */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            已有账户？{' '}
            <Link to="/login" className="text-blue-600 hover:text-blue-700 font-medium">
              立即登录
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

