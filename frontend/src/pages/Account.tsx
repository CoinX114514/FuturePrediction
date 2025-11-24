import { useState } from 'react'
import MainLayout from '../components/layout/MainLayout'
import { useNavigate } from 'react-router-dom'

export default function Account() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'favorites' | 'history' | 'posts' | 'drafts'>('favorites')

  // Mock User Data
  const user = {
    nickname: 'Colin_Trader',
    user_id: '8849201',
    role: 'VIP 会员',
    roleType: 2,
    expireDate: '2025-12-31',
    avatar: null
  }

  // Mock List Data
  const items = [
    { id: 1, title: '沪深300股指期货(IF2312) 关键点位分析', date: '2023-11-24 10:30', author: '管理员', type: 'buy' },
    { id: 2, title: '螺纹钢 RB2401 震荡下行趋势确立', date: '2023-11-23 15:45', author: '管理员', type: 'sell' },
    { id: 3, title: '黄金 AU2402 避险情绪升温', date: '2023-11-23 09:15', author: '分析师A', type: 'buy' },
  ]

  return (
    <MainLayout user={{ nickname: user.nickname, user_role: user.roleType }} onLogout={() => {}}>
      <div className="max-w-5xl mx-auto">
        {/* Header Profile Section */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-200 mb-6 flex items-center gap-8">
           {/* Avatar */}
           <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-3xl font-bold border-4 border-blue-50 shadow-inner">
              {user.avatar || user.nickname[0]}
           </div>
           
           {/* Info */}
           <div className="flex-1">
              <div className="flex items-center gap-4 mb-2">
                 <h1 className="text-2xl font-bold text-gray-900">{user.nickname}</h1>
                 <span className="px-3 py-1 bg-amber-100 text-amber-700 text-xs font-bold rounded-full border border-amber-200">
                    {user.role}
                 </span>
              </div>
              <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm text-gray-500">
                 <p>账户 ID: <span className="font-mono text-gray-700">{user.user_id}</span></p>
                 <p>VIP 到期: <span className="font-mono text-gray-700">{user.expireDate}</span></p>
                 <p>账户权限: <span className="text-green-600">已激活</span></p>
              </div>
           </div>

           {/* Action */}
           <div>
              <button className="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-medium text-sm">
                 编辑资料
              </button>
           </div>
        </div>

        {/* Content Tabs & List */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 min-h-[500px] flex flex-col">
           {/* Tabs */}
           <div className="flex border-b border-gray-100">
              {[
                { id: 'favorites', label: '最近收藏' },
                { id: 'history', label: '浏览历史记录' },
                { id: 'posts', label: '我的帖子' },
                { id: 'drafts', label: '草稿箱' }
              ].map(tab => (
                 <button
                   key={tab.id}
                   onClick={() => setActiveTab(tab.id as any)}
                   className={`flex-1 py-4 text-sm font-medium transition-all relative ${
                     activeTab === tab.id 
                       ? 'text-blue-600 bg-blue-50/50' 
                       : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                   }`}
                 >
                    {tab.label}
                    {activeTab === tab.id && (
                       <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600 mx-auto w-1/2 rounded-t-full"></div>
                    )}
                 </button>
              ))}
           </div>

           {/* List Content */}
           <div className="p-4">
              {items.map(item => (
                 <div 
                    key={item.id} 
                    onClick={() => navigate(`/signal/${item.id}`)}
                    className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-xl cursor-pointer group transition-colors border-b border-gray-50 last:border-0"
                 >
                    <div className="flex items-center gap-4">
                       <div className={`w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-xs ${
                          item.type === 'buy' ? 'bg-red-500' : 'bg-green-500'
                       }`}>
                          {item.type === 'buy' ? '多' : '空'}
                       </div>
                       <div>
                          <h3 className="font-bold text-gray-800 group-hover:text-blue-600 transition-colors mb-1">{item.title}</h3>
                          <p className="text-xs text-gray-400">发布者: {item.author} · {item.date}</p>
                       </div>
                    </div>
                    <div className="text-gray-400 group-hover:text-blue-400 group-hover:translate-x-1 transition-all">
                       <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
                    </div>
                 </div>
              ))}
              
              {/* Empty State Placeholder */}
              <div className="hidden p-12 text-center text-gray-400">
                 暂无数据
              </div>
           </div>
        </div>
      </div>
    </MainLayout>
  )
}

