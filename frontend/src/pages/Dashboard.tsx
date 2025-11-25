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
  
  useEffect(() => {
    console.log('[Dashboard] useEffect 触发', { hasUserInfo: !!userInfo })
    
    /** 从后端获取用户信息。 */
    const fetchUserInfo = async () => {
      if (!userInfo) {
        console.log('[Dashboard] 开始获取用户信息...')
        const startTime = Date.now()
        
        // 设置超时保护
        const timeoutId = setTimeout(() => {
          console.warn('[Dashboard] 获取用户信息超时（5秒）')
        }, 5000)
        
        try {
          const user = await getCurrentUser()
          clearTimeout(timeoutId)
          const elapsed = Date.now() - startTime
          console.log(`[Dashboard] 用户信息获取成功，耗时: ${elapsed}ms`, user)
          console.log(`[Dashboard] 用户角色: ${user.user_role} (1=普通用户, 2=VIP会员, 3=超级管理员)`)
          setUserInfo(user)
        } catch (err) {
          clearTimeout(timeoutId)
          const elapsed = Date.now() - startTime
          console.error(`[Dashboard] 获取用户信息失败，耗时: ${elapsed}ms`, err)
          // 获取失败时不设置默认值，让页面显示加载状态或错误提示
        }
      } else {
        console.log('[Dashboard] 已有用户信息，跳过获取', userInfo)
      }
    }
    
    fetchUserInfo()
  }, [userInfo])

  /** 从后端获取帖子列表。 */
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        setLoading(true)
        console.log('[Dashboard] 开始获取帖子列表...')
        const response = await getPosts(1, 20)
        console.log('[Dashboard] 帖子列表获取成功', response)
        setPosts(response.posts)
      } catch (err) {
        console.error('[Dashboard] 获取帖子列表失败', err)
      } finally {
        setLoading(false)
      }
    }
    
    fetchPosts()
  }, [])

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  /** 将后端帖子数据转换为 SignalCard 需要的格式。 */
  const convertPostToSignal = (post: Post) => {
    // 根据止损价和现价判断是做多还是做空
    // 如果现价 > 止损价，通常是做多；如果现价 < 止损价，通常是做空
    // 这里简化处理：如果有止盈价且止盈价 > 止损价，则为做多；否则为做空
    const isBuy = post.take_profit ? post.take_profit > post.stop_loss : true
    
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
      currentPrice: post.current_price || post.stop_loss, // 如果没有现价，使用止损价作为默认值
      advice: post.suggestion || '暂无建议',
      time: timeStr,
      type: (isBuy ? 'buy' : 'sell') as 'buy' | 'sell',
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
              <h2 className="text-2xl font-bold mb-2">早安，{userInfo?.nickname || '交易员'}</h2>
              <p className="opacity-90">今日市场情绪偏多，建议关注金融期货板块。</p>
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
