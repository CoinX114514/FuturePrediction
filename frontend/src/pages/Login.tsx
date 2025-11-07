/** 登录页面组件。

提供用户登录功能，支持手机号和邮箱登录。
*/

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login } from '../services/authService'

/** 登录表单数据接口。 */
interface LoginFormData {
  /** 手机号或邮箱。 */
  credential: string
  /** 密码。 */
  password: string
  /** 登录方式：phone 或 email。 */
  loginType: 'phone' | 'email'
}

/**
 * 登录页面组件。
 * 
 * @returns JSX 元素。
 */
export default function Login() {
  /** 导航钩子。 */
  const navigate = useNavigate()
  
  /** 登录表单数据。 */
  const [formData, setFormData] = useState<LoginFormData>({
    credential: '',
    password: '',
    loginType: 'phone',
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
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }))
    setError(null)
  }

  /**
   * 处理表单提交。
   * 
   * @param e - 表单提交事件。
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const loginData = formData.loginType === 'phone'
        ? { phone_number: formData.credential, password: formData.password }
        : { email: formData.credential, password: formData.password }

      await login(loginData)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || '登录失败，请检查您的凭证')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
        {/* 标题 */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">欢迎回来</h1>
          <p className="text-gray-600">登录您的账户以继续</p>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* 登录表单 */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* 登录方式选择 */}
          <div>
            <label htmlFor="loginType" className="block text-sm font-medium text-gray-700 mb-2">
              登录方式
            </label>
            <select
              id="loginType"
              name="loginType"
              value={formData.loginType}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="phone">手机号登录</option>
              <option value="email">邮箱登录</option>
            </select>
          </div>

          {/* 手机号/邮箱输入 */}
          <div>
            <label htmlFor="credential" className="block text-sm font-medium text-gray-700 mb-2">
              {formData.loginType === 'phone' ? '手机号' : '邮箱地址'}
            </label>
            <input
              type={formData.loginType === 'phone' ? 'tel' : 'email'}
              id="credential"
              name="credential"
              value={formData.credential}
              onChange={handleChange}
              required
              placeholder={formData.loginType === 'phone' ? '请输入11位手机号' : '请输入邮箱地址'}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 密码输入 */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              密码
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="请输入密码"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* 提交按钮 */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '登录中...' : '登录'}
          </button>
        </form>

        {/* 注册链接 */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            还没有账户？{' '}
            <Link to="/register" className="text-blue-600 hover:text-blue-700 font-medium">
              立即注册
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

