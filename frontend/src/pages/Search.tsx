/** 搜索合约页面。

提供合约搜索功能。
*/

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import { getCurrentUser } from '../services/authService'
import { getPosts, Post } from '../services/postService'
import SignalCard from '../components/SignalCard'

export default function Search() {
  const navigate = useNavigate()
  
  /** 用户信息状态。 */
  const [userInfo, setUserInfo] = useState<any>(null)
  
  /** 搜索关键词状态。 */
  const [searchKeyword, setSearchKeyword] = useState<string>('')
  
  /** 帖子列表状态。 */
  const [posts, setPosts] = useState<Post[]>([])
  
  /** 加载状态。 */
  const [loading, setLoading] = useState(true)
  
  /** 从后端获取用户信息（仅在组件首次加载时调用）。 */
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getCurrentUser()
        setUserInfo(user)
      } catch (err: any) {
        console.error('[Search] 获取用户信息失败', err)
        // 如果是认证错误（401），authService 的响应拦截器会自动处理跳转
        // 这里不需要额外操作，拦截器会清除 token 并跳转到登录页
      } finally {
        setLoading(false)
      }
    }
    
    fetchUser()
  }, []) // 空依赖数组，只在组件首次加载时执行
  
  /** 执行搜索（当搜索关键词变化时调用）。 */
  useEffect(() => {
    // 如果用户信息未加载完成，不执行搜索
    if (loading || !userInfo) {
      return
    }
    
    const performSearch = async () => {
      if (!searchKeyword.trim()) {
        setPosts([])
        return
      }
      
      try {
        const response = await getPosts(1, 100, undefined, searchKeyword.trim())
        setPosts(response.posts || [])
      } catch (err: any) {
        console.error('[Search] 搜索失败', err)
        // 如果是认证错误（401），authService 的响应拦截器会自动处理跳转
        // 其他错误，清空搜索结果
        if (err.response?.status !== 401) {
          setPosts([])
        }
      }
    }
    
    performSearch()
  }, [searchKeyword, loading, userInfo]) // 依赖搜索关键词、加载状态和用户信息

  /** 现价与后端同步：有搜索结果时每 5 分钟刷新列表 */
  const PRICE_REFRESH_INTERVAL_MS = 5 * 60 * 1000
  useEffect(() => {
    if (!userInfo || loading || !searchKeyword.trim()) return
    const refresh = async () => {
      try {
        const response = await getPosts(1, 100, undefined, searchKeyword.trim())
        setPosts(response.posts || [])
      } catch {
        // 静默失败，保留当前列表
      }
    }
    const timer = setInterval(refresh, PRICE_REFRESH_INTERVAL_MS)
    return () => clearInterval(timer)
  }, [searchKeyword, userInfo, loading])
  
  /** 处理搜索输入变化。 */
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchKeyword(e.target.value)
  }
  
  /** 处理搜索框清空。 */
  const handleSearchClear = () => {
    setSearchKeyword('')
  }
  
  /** 处理登出。 */
  const handleLogout = async () => {
    const { logout } = await import('../services/authService')
    await logout()
    navigate('/login')
  }
  
  /** 将后端帖子数据转换为 SignalCard 需要的格式。 */
  const convertPostToSignal = (post: Post) => {
    // 使用帖子中的 direction 字段，如果没有则默认为做多
    const direction = post.direction || 'buy'
    
    // 格式化时间
    const publishTime = new Date(post.publish_time)
    const timeStr = `${publishTime.getHours().toString().padStart(2, '0')}:${publishTime.getMinutes().toString().padStart(2, '0')}`
    
    // 从合约代码提取合约名称（简化处理，实际可以从合约表获取）
    const contractNameMap: Record<string, string> = {
      'IF': '沪深300股指',
      'RB': '螺纹钢',
      'AU': '黄金',
      'CU': '铜',
      'SC': '原油',
      'I': '铁矿石',
      'SS': '不锈钢',
      'TA': 'PTA',
    }
    const contractPrefix = post.contract_code.substring(0, 2)
    const contractName = contractNameMap[contractPrefix] || post.contract_code
    
    return {
      id: post.post_id,
      title: post.title,
      contractName,
      contractCode: post.contract_code,
      strikePrice: post.strike_price,
      stopLoss: post.stop_loss,
      currentPrice: post.current_price, // 允许为 undefined，SignalCard 会显示 "/"
      advice: post.suggestion || '暂无建议',
      time: timeStr,
      type: direction as 'buy' | 'sell',
    }
  }
  
  // 如果用户信息未加载，显示加载状态
  if (loading || !userInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-500 font-medium">加载中...</p>
        </div>
      </div>
    )
  }
  
  return (
    <MainLayout user={userInfo} onLogout={handleLogout}>
      <div className="flex gap-6 h-[calc(100vh-7rem)]">
        {/* 中间：搜索和结果列表 */}
        <div className="flex-1 overflow-y-auto pr-2">
          {/* 页面标题 */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">搜索合约</h1>
            <p className="text-gray-600">输入合约代码或名称进行搜索</p>
          </div>
          
          {/* 搜索框 */}
          <div className="mb-6">
            <div className="relative">
              <input
                type="text"
                placeholder="搜索合约代码或名称（如：SS2611、不锈钢）"
                value={searchKeyword}
                onChange={handleSearchChange}
                className="w-full px-4 py-3 pl-12 pr-10 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                autoFocus
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              {searchKeyword && (
                <button
                  onClick={handleSearchClear}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          </div>
          
          {/* 搜索结果 */}
          {searchKeyword.trim() ? (
            <div>
              {posts.length > 0 ? (
                <div className="space-y-4">
                  <div className="text-sm text-gray-600 mb-4">
                    找到 {posts.length} 个相关结果
                  </div>
                  {posts.map((post) => {
                    const signal = convertPostToSignal(post)
                    return (
                      <div key={signal.id} onClick={() => navigate(`/signal/${signal.id}`)} className="cursor-pointer block">
                        <SignalCard {...signal} />
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <p className="text-lg font-medium">未找到相关结果</p>
                  <p className="text-sm mt-2">请尝试其他关键词</p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <p className="text-lg font-medium">请输入搜索关键词</p>
              <p className="text-sm mt-2">搜索合约代码或名称，例如：SS2611、IF2312、不锈钢</p>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  )
}
