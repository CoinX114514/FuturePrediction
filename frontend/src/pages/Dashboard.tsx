/** 交易仪表板页面组件。 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import SignalCard from '../components/SignalCard'
import { logout, getCurrentUser } from '../services/authService'
import { getPosts, Post } from '../services/postService'

export default function Dashboard() {
  console.log("Rendering Dashboard Component");
  const navigate = useNavigate()

  /** 用户信息状态。始终从后端获取，不使用硬编码的开发模式数据。 */
  const [userInfo, setUserInfo] = useState<any>(null)
  
  /** 帖子列表状态。 */
  const [posts, setPosts] = useState<Post[]>([])
  
  /** 加载状态。 */
  const [loading, setLoading] = useState(true)
  
  /** 搜索关键词状态。 */
  const [searchKeyword, setSearchKeyword] = useState<string>('')
  
  // 并行获取用户信息和帖子列表，提高加载速度
  useEffect(() => {
    const fetchAllData = async () => {
      // 如果已有用户信息，只获取帖子列表
      if (userInfo) {
        try {
          setLoading(true)
          const response = await getPosts(1, 20, undefined, searchKeyword || undefined)
          setPosts(response.posts)
        } catch (err) {
          console.error('[Dashboard] 获取帖子列表失败', err)
        } finally {
          setLoading(false)
        }
        return
      }

      // 并行获取用户信息和帖子列表
      const startTime = Date.now()
      try {
        const [user, postsResponse] = await Promise.all([
          getCurrentUser().catch((err: any) => {
            // 如果是认证错误，跳转到登录页
            if (err?.response?.status === 401 || err?.code === 'ECONNABORTED') {
              navigate('/login')
              throw err
            }
            throw err
          }),
          getPosts(1, 20, undefined, searchKeyword || undefined)
        ])
        
        const elapsed = Date.now() - startTime
        console.log(`[Dashboard] 数据获取成功，耗时: ${elapsed}ms`)
        setUserInfo(user)
        setPosts(postsResponse.posts)
      } catch (err: any) {
        console.error(`[Dashboard] 获取数据失败`, err)
        // 如果是认证错误，已经跳转到登录页，不需要额外处理
        if (err?.response?.status !== 401 && err?.code !== 'ECONNABORTED') {
          // 其他错误，显示错误提示
          console.warn('[Dashboard] 获取数据失败，但继续加载页面')
        }
      } finally {
        setLoading(false)
      }
    }
    
    fetchAllData()
  }, [userInfo, navigate, searchKeyword])

  /** 现价与后端同步：每 5 分钟刷新帖子列表（与后端 PRICE_UPDATE_INTERVAL_MINUTES=5 一致） */
  const PRICE_REFRESH_INTERVAL_MS = 5 * 60 * 1000

  useEffect(() => {
    if (!userInfo) return

    const refreshPrices = async () => {
      try {
        const response = await getPosts(1, 20, undefined, searchKeyword || undefined)
        setPosts(response.posts)
      } catch (err) {
        console.error('[Dashboard] 刷新现价失败', err)
      }
    }

    const timer = setInterval(refreshPrices, PRICE_REFRESH_INTERVAL_MS)
    return () => clearInterval(timer)
  }, [userInfo, searchKeyword])
  
  /** 处理搜索输入变化。 */
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchKeyword(e.target.value)
  }
  
  /** 处理搜索框清空。 */
  const handleSearchClear = () => {
    setSearchKeyword('')
  }

  // 帖子列表获取已合并到上面的 useEffect 中，避免重复请求

  const handleLogout = async () => {
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
  if (!userInfo) {
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
        {/* 中间：信息流列表 */}
        <div className="flex-1 overflow-y-auto pr-2">
           {/* 欢迎横幅 (可选) */}
           <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-6 mb-6 text-white shadow-lg">
              <h2 className="text-2xl font-bold mb-2">您好，{userInfo?.nickname || '交易员'}</h2>
              <p className="opacity-90">欢迎使用Mambo期货交易系统，祝您交易顺利。</p>
           </div>
           
           {/* 搜索框 */}
           <div className="mb-6">
             <div className="relative">
               <input
                 type="text"
                 placeholder="搜索合约代码或名称（如：TA2601、PTA）"
                 value={searchKeyword}
                 onChange={handleSearchChange}
                 className="w-full px-4 py-3 pl-12 pr-10 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
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

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-500 font-medium">加载帖子中...</p>
        </div>
        </div>
          ) : posts.length === 0 ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center text-gray-400">
                <p className="text-lg font-medium">暂无帖子</p>
                <p className="text-sm mt-2">管理员发布帖子后，将在这里显示</p>
          </div>
            </div>
          ) : (
            <div className="space-y-4">
              {posts.map(post => {
                const signal = convertPostToSignal(post)
                return (
                  <div key={signal.id} onClick={() => navigate(`/signal/${signal.id}`)} className="cursor-pointer block">
                    <SignalCard {...signal} />
                  </div>
                )
              })}
            </div>
          )}
              </div>
              
        {/* 右侧：退出登录 */}
        <div className="w-80 flex flex-col gap-4 h-full">
          {/* 退出登录按钮 */}
                 <button 
            onClick={handleLogout}
            className="w-full py-3 bg-white border border-gray-200 text-red-500 font-bold rounded-xl hover:bg-red-50 hover:border-red-200 transition-all shadow-sm flex items-center justify-center gap-2"
                 >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
            退出登录
                 </button>
              </div>
           </div>
    </MainLayout>
  )
}
