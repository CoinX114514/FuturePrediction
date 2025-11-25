import { useState, useEffect } from 'react'
import MainLayout from '../components/layout/MainLayout'
import { useNavigate } from 'react-router-dom'
import { getCurrentUser } from '../services/authService'
import { getCollections, getBrowseHistory, getUserPosts, getDrafts, PostItem } from '../services/accountService'

export default function Account() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'favorites' | 'history' | 'posts' | 'drafts'>('favorites')
  
  /** 用户信息状态。从后端获取真实数据。 */
  const [userInfo, setUserInfo] = useState<any>(null)
  
  /** 列表数据状态。 */
  const [items, setItems] = useState<any[]>([])
  
  /** 加载状态。 */
  const [loading, setLoading] = useState(false)

  /** 根据用户角色获取角色显示名称。 */
  const getRoleName = (userRole?: number): string => {
    if (!userRole) return '普通用户'
    switch (userRole) {
      case 1:
        return '普通用户'
      case 2:
        return 'VIP会员'
      case 3:
        return '超级管理员'
      default:
        return '普通用户'
    }
  }

  /** 从后端获取用户信息。 */
  useEffect(() => {
    const fetchUserInfo = async () => {
      if (!userInfo) {
        try {
          const user = await getCurrentUser()
          console.log('[Account] 用户信息获取成功', user)
          setUserInfo(user)
        } catch (err) {
          console.error('[Account] 获取用户信息失败', err)
        }
      }
    }
    fetchUserInfo()
  }, [userInfo])

  /** 根据当前标签页从后端获取数据。 */
  useEffect(() => {
    const fetchData = async () => {
      if (!userInfo) return
      
      setLoading(true)
      try {
        let data: any[] = []
        
        switch (activeTab) {
          case 'favorites':
            const collections = await getCollections(1, 20)
            data = collections.posts.map((post: PostItem) => ({
              id: post.post_id,
              title: post.title,
              date: new Date(post.publish_time).toLocaleString('zh-CN'),
              author: '管理员',
              type: post.current_price && post.current_price > post.stop_loss ? 'buy' : 'sell',
            }))
            break
          case 'history':
            const history = await getBrowseHistory(1, 20)
            data = history.posts.map((post: PostItem) => ({
              id: post.post_id,
              title: post.title,
              date: new Date(post.publish_time).toLocaleString('zh-CN'),
              author: '管理员',
              type: post.current_price && post.current_price > post.stop_loss ? 'buy' : 'sell',
            }))
            break
          case 'posts':
            const posts = await getUserPosts(1, 20)
            data = posts.posts.map((post: any) => ({
              id: post.post_id,
              title: post.title,
              date: new Date(post.publish_time).toLocaleString('zh-CN'),
              author: post.author_nickname || '管理员',
              type: post.current_price && post.current_price > post.stop_loss ? 'buy' : 'sell',
            }))
            break
          case 'drafts':
            const drafts = await getDrafts()
            data = drafts.drafts.map((draft: any) => ({
              id: draft.draft_id,
              title: draft.title || '无标题',
              date: new Date(draft.update_time).toLocaleString('zh-CN'),
              author: '我',
              type: 'buy' as const,
            }))
            break
        }
        
        setItems(data)
      } catch (err) {
        console.error(`[Account] 获取${activeTab}数据失败`, err)
        setItems([])
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [activeTab, userInfo])

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
    <MainLayout user={userInfo} onLogout={() => {}}>
      <div className="max-w-5xl mx-auto">
        {/* Header Profile Section */}
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-200 mb-6 flex items-center gap-8">
           {/* Avatar */}
           <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-3xl font-bold border-4 border-blue-50 shadow-inner">
              {userInfo.avatar_url || userInfo.nickname?.[0] || 'U'}
           </div>
           
           {/* Info */}
           <div className="flex-1">
              <div className="flex items-center gap-4 mb-2">
                 <h1 className="text-2xl font-bold text-gray-900">{userInfo.nickname || '用户'}</h1>
                 <span className="px-3 py-1 bg-amber-100 text-amber-700 text-xs font-bold rounded-full border border-amber-200">
                    {getRoleName(userInfo.user_role)}
                 </span>
              </div>
              <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm text-gray-500">
                 <p>账户 ID: <span className="font-mono text-gray-700">{userInfo.user_id}</span></p>
                 {userInfo.user_role === 2 && userInfo.member_expire_time && (
                   <p>VIP 到期: <span className="font-mono text-gray-700">{new Date(userInfo.member_expire_time).toLocaleDateString('zh-CN')}</span></p>
                 )}
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
              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-2 text-gray-500 text-sm">加载中...</p>
                  </div>
                </div>
              ) : items.length === 0 ? (
                <div className="p-12 text-center text-gray-400">
                  <p className="text-lg font-medium">暂无数据</p>
                  <p className="text-sm mt-2">这里将显示您的{activeTab === 'favorites' ? '收藏' : activeTab === 'history' ? '浏览历史' : activeTab === 'posts' ? '发布的帖子' : '草稿'}</p>
                </div>
              ) : (
                items.map(item => (
                  <div 
                     key={item.id} 
                     onClick={() => {
                       if (activeTab === 'drafts') {
                         // 草稿跳转到编辑页面（暂时跳转到详情页）
                         navigate(`/admin/publish?draft=${item.id}`)
                       } else {
                         navigate(`/signal/${item.id}`)
                       }
                     }}
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
                ))
              )}
           </div>
        </div>
      </div>
    </MainLayout>
  )
}

