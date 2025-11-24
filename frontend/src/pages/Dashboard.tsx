/** 交易仪表板页面组件。 */
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Rankings from '../components/Rankings'
import MainLayout from '../components/layout/MainLayout'
import SignalCard from '../components/SignalCard'
import { logout, getCurrentUser } from '../services/authService'

export default function Dashboard() {
  console.log("Rendering Dashboard Component");
  const navigate = useNavigate()

  const isDevMode = (import.meta as any).env?.MODE === 'development' || 
                    (import.meta as any).env?.VITE_DEV_MODE === 'true'

  const [userInfo, setUserInfo] = useState<any>(isDevMode ? {
    user_id: 1,
    phone_number: '13800138000',
    nickname: '开发用户',
    user_role: 2, // VIP
  } : null)
  
  useEffect(() => {
    const fetchUserInfo = async () => {
      if (!isDevMode && !userInfo) {
        try {
          const user = await getCurrentUser()
          setUserInfo(user)
        } catch (err) {
          console.error('Failed to get user info:', err)
        }
      }
    }
    fetchUserInfo()
  }, [isDevMode, userInfo])

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  // Mock Data for Signals
  const signals = [
    {
      id: 1,
      title: '今日主力推荐',
      contractName: '沪深300股指',
      contractCode: 'IF2312',
      stopLoss: 3520.0,
      currentPrice: 3580.2,
      advice: '技术指标出现金叉，MACD底背离，建议在3550附近分批建仓做多，第一目标位3620。',
      time: '10:30',
      type: 'buy' as const
    },
    {
      id: 2,
      title: '趋势预警',
      contractName: '螺纹钢',
      contractCode: 'RB2401',
      stopLoss: 3850,
      currentPrice: 3810,
      advice: '受房地产数据疲软影响，上方抛压沉重，建议反弹至3830附近尝试做空。',
      time: '09:45',
      type: 'sell' as const
    },
    {
      id: 3,
      title: '波动套利机会',
      contractName: '铁矿石',
      contractCode: 'I2401',
      strikePrice: 950,
      stopLoss: 920,
      currentPrice: 935.5,
      advice: '短期维持震荡格局，区间920-960高抛低吸。',
      time: '09:15',
      type: 'buy' as const
    },
    {
      id: 4,
      title: '日内短线',
      contractName: '原油',
      contractCode: 'SC2401',
      stopLoss: 580.0,
      currentPrice: 588.5,
      advice: '受地缘政治消息影响，早盘高开，建议观望或轻仓试多。',
      time: '11:00',
      type: 'buy' as const
    }
  ]

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

          <div className="space-y-4">
             {signals.map(signal => (
               <div key={signal.id} onClick={() => navigate(`/signal/${signal.id}`)} className="cursor-pointer block">
                 <SignalCard {...signal} />
               </div>
             ))}
          </div>
        </div>

        {/* 右侧：板块排行 + 退出 */}
        <div className="w-80 flex flex-col gap-4 h-full">
          {/* 板块排行组件 - 占据大部分高度 */}
          <div className="flex-1 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
             <Rankings isMember={userInfo?.user_role >= 2} />
          </div>

          {/* 退出登录按钮 - 底部 */}
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
