import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import { getCurrentUser } from '../services/authService'
import { getPostById, deletePost } from '../services/postService'
import KlineChart from '../components/KlineChart'

export default function SignalDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  
  /** 用户信息状态。从后端获取真实数据。 */
  const [userInfo, setUserInfo] = useState<any>(null)
  
  /** 帖子详情状态。 */
  const [postDetail, setPostDetail] = useState<any>(null)
  
  /** 加载状态。 */
  const [loading, setLoading] = useState(true)
  const [deletingPost, setDeletingPost] = useState(false)

  /** 从后端获取用户信息和帖子详情。 */
  useEffect(() => {
    const fetchData = async () => {
      try {
        // 并行获取用户信息和帖子详情
        const [user, post] = await Promise.all([
          getCurrentUser(),
          getPostById(Number(id))
        ])
        setUserInfo(user)
        setPostDetail(post)
      } catch (err) {
        console.error('[SignalDetail] 获取数据失败', err)
      } finally {
        setLoading(false)
      }
    }
    
    if (id) {
      fetchData()
    }
  }, [id])

  /** 现价与后端同步：每 5 分钟刷新帖子详情（现价、止损等与主页/K 线一致） */
  const PRICE_REFRESH_INTERVAL_MS = 5 * 60 * 1000
  useEffect(() => {
    if (!id || !postDetail) return
    const refreshDetail = async () => {
      try {
        const post = await getPostById(Number(id))
        setPostDetail(post)
      } catch {
        // 静默失败
      }
    }
    const timer = setInterval(refreshDetail, PRICE_REFRESH_INTERVAL_MS)
    return () => clearInterval(timer)
  }, [id, postDetail?.post_id])

  /** 从合约代码提取合约名称。 */
  const getContractName = (contractCode: string): string => {
    const contractNameMap: Record<string, string> = {
      'IF': '沪深300股指',
      'RB': '螺纹钢',
      'AU': '黄金',
      'CU': '铜',
      'SC': '原油',
      'I': '铁矿石',
    }
    const contractPrefix = contractCode.substring(0, 2)
    return contractNameMap[contractPrefix] || contractCode
  }

  /** 格式化发布时间。 */
  const formatPublishTime = (timeStr: string): string => {
    const date = new Date(timeStr)
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
  }

  // 如果数据未加载，显示加载状态
  if (loading || !userInfo || !postDetail) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-500 font-medium">加载中...</p>
        </div>
      </div>
    )
  }

  /** 判断是否显示VIP升级widget：只对普通用户（user_role === 1）显示。 */
  const showVipUpgrade = userInfo.user_role === 1
  /** 管理员（含超级管理员）可编辑任意帖子；编辑按钮对所有管理员可见 */
  const isAdmin = userInfo.user_role >= 3

  const handleDeletePost = async () => {
    if (!postDetail) return
    if (!confirm('确定删除该帖子吗？删除后将无法恢复。')) return

    setDeletingPost(true)
    try {
      await deletePost(postDetail.post_id)
      alert('帖子已删除')
      navigate('/dashboard')
    } catch (err) {
      console.error('[SignalDetail] 删除帖子失败', err)
      alert('删除失败，请稍后重试')
    } finally {
      setDeletingPost(false)
    }
  }

  return (
    <MainLayout user={userInfo} onLogout={() => {}}>
      <div className="grid grid-cols-12 gap-6 max-w-7xl mx-auto h-[calc(100vh-8rem)]">
        {/* Left Column: Content */}
        <div className="col-span-9 bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-full">
           {/* Header */}
           <div className="p-6 border-b border-gray-100">
              <div className="flex items-center gap-3 mb-3">
                 <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded">
                    {getContractName(postDetail.contract_code)}
                 </span>
                 <span className="text-sm text-gray-500">{postDetail.contract_code}</span>
                 <span className="ml-auto text-sm text-gray-400">{formatPublishTime(postDetail.publish_time)}</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-4">{postDetail.title}</h1>
              
              <div className="flex flex-wrap gap-4 items-center">
                 {/* 现价：始终展示，与止损参考并排；无数据时显示 — */}
                 <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg border border-blue-100">
                   <span className="text-xs text-blue-500">现价</span>
                   <span className="font-mono font-bold text-blue-700">
                     {postDetail.current_price != null ? postDetail.current_price.toLocaleString() : '—'}
                   </span>
                 </div>
                 <div className="flex items-center gap-2 px-4 py-2 bg-red-50 rounded-lg border border-red-100">
                   <span className="text-xs text-red-500">止损参考</span>
                   <span className="font-mono font-bold text-red-700">{postDetail.stop_loss}</span>
                 </div>
                 {postDetail.take_profit && (
                   <div className="flex items-center gap-2 px-4 py-2 bg-green-50 rounded-lg border border-green-100">
                      <span className="text-xs text-green-500">止盈参考</span>
                      <span className="font-mono font-bold text-green-700">{postDetail.take_profit}</span>
                   </div>
                 )}
              </div>
           </div>

           {/* Scrollable Content Area */}
           <div className="flex-1 overflow-y-auto p-8">
              {/* K 线图表 */}
              <div className="w-full bg-white rounded-xl border-2 border-gray-200 p-4 mb-8">
                <div className="mb-2 flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-700">
                    {postDetail.contract_code} 历史 K 线图
                  </h3>
                  {postDetail.k_line_image && (
                    <a 
                      href={postDetail.k_line_image} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:text-blue-800"
                    >
                      查看原图
                    </a>
                  )}
                </div>
                {postDetail.contract_code ? (
                  <KlineChart 
                    contractCode={postDetail.contract_code} 
                    height={500}
                    period={365}
                  />
              ) : (
                  <div className="w-full h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200 flex items-center justify-center">
                    <div className="text-center text-gray-400">
                      <svg className="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                      </svg>
                      <span className="text-sm font-medium">暂无合约代码</span>
                    </div>
                </div>
              )}
              </div>

              {/* Text Content */}
              <div className="prose max-w-none text-gray-700 whitespace-pre-line leading-relaxed">
                 {postDetail.content}
              </div>
           </div>

           {/* Footer Actions：管理员必显「编辑帖子」+「删除帖子」 */}
           <div className="p-4 border-t border-gray-100 bg-gray-50 flex justify-between items-center flex-wrap gap-2">
              <div className="flex flex-wrap gap-2 items-center">
                <button
                  type="button"
                  onClick={() => navigate(-1)}
                  className="px-4 py-2 text-gray-500 hover:bg-gray-200 rounded-lg transition-colors text-sm"
                >
                  ← 返回列表
                </button>
                {isAdmin && (
                  <button
                    type="button"
                    onClick={() => navigate(`/admin/publish?post=${postDetail.post_id}`)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium shadow-sm"
                  >
                    编辑帖子
                  </button>
                )}
                {isAdmin && (
                  <button
                    type="button"
                    onClick={handleDeletePost}
                    disabled={deletingPost}
                    className="px-4 py-2 text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors text-sm border border-red-200 disabled:opacity-50"
                  >
                    {deletingPost ? '删除中...' : '删除帖子'}
                  </button>
                )}
              </div>
              <div className="flex gap-3">
                 <button className={`flex items-center gap-2 px-4 py-2 border rounded-lg transition-colors text-sm ${
                   postDetail.is_collected 
                     ? 'bg-red-50 border-red-200 text-red-600' 
                     : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                 }`}>
                    <svg className="w-5 h-5" fill={postDetail.is_collected ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
                    <span>{postDetail.is_collected ? '已收藏' : '收藏'}</span>
                 </button>
              </div>
           </div>
        </div>

        {/* Right Column: Author Info */}
        <div className="col-span-3 flex flex-col gap-6">
           <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
              <div className="w-20 h-20 mx-auto bg-gray-200 rounded-full mb-4 overflow-hidden">
                 {postDetail.author_avatar ? (
                   <img src={postDetail.author_avatar} alt={postDetail.author_nickname} className="w-full h-full object-cover" />
                 ) : (
                   <svg className="w-full h-full text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                 )}
              </div>
              <h3 className="font-bold text-gray-900 text-lg">{postDetail.author_nickname || '管理员'}</h3>
              <p className="text-xs text-gray-500 mt-1">认证分析师 / 资深交易员</p>
              
              <button className="mt-4 w-full py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 font-medium text-sm transition-colors">
                 查看主页
              </button>
           </div>

           {/* VIP升级widget：只对普通用户显示 */}
           {showVipUpgrade && (
             <div className="bg-blue-600 rounded-xl shadow-lg p-6 text-white">
                <h4 className="font-bold text-lg mb-2">开通 VIP 会员</h4>
                <p className="text-sm opacity-90 mb-4">解锁更多深度分析和实时交易信号提示。</p>
                <button className="w-full py-2 bg-white text-blue-600 rounded-lg font-bold hover:bg-gray-50 transition-colors text-sm">
                   立即升级
                </button>
             </div>
           )}
        </div>
      </div>
    </MainLayout>
  )
}

