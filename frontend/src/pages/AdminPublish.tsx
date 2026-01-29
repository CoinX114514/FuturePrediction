/** 帖子编辑页（仅编辑已有帖子）。

超级管理员从详情页底部「编辑内容」进入；结构与详情页一致，展示日线 K 线与现价（只读），可编辑标题、止损、止盈、方向、正文。
*/

import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import { getCurrentUser } from '../services/authService'
import { getPostById, updatePost, deletePost, Post } from '../services/postService'
import KlineChart from '../components/KlineChart'

/** 合约代码到中文名称的映射（与详情页一致）。 */
function getContractName(contractCode: string): string {
  const contractNameMap: Record<string, string> = {
    IF: '沪深300股指',
    RB: '螺纹钢',
    AU: '黄金',
    CU: '铜',
    SC: '原油',
    I: '铁矿石',
    PP: '聚丙烯',
  }
  const prefix = contractCode.substring(0, 2)
  return contractNameMap[prefix] || contractCode
}

export default function AdminPublish() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const postIdParam = searchParams.get('post')

  const [userInfo, setUserInfo] = useState<any>(null)
  const [post, setPost] = useState<Post | null>(null)
  const [loading, setLoading] = useState(true)
  const [redirectChecked, setRedirectChecked] = useState(false)

  /** 可编辑字段（现价只读，不在此处） */
  const [title, setTitle] = useState('')
  const [stopLoss, setStopLoss] = useState('')
  const [takeProfit, setTakeProfit] = useState('')
  const [direction, setDirection] = useState<'buy' | 'sell'>('buy')
  const [content, setContent] = useState('')
  const [updating, setUpdating] = useState(false)
  const [deleting, setDeleting] = useState(false)

  /** 无 post 参数时重定向到主页 */
  useEffect(() => {
    if (!postIdParam) {
      setRedirectChecked(true)
      navigate('/dashboard', { replace: true })
      return
    }
    setRedirectChecked(true)
  }, [postIdParam, navigate])

  /** 获取当前用户 */
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getCurrentUser()
        setUserInfo(user)
      } catch {
        navigate('/login', { replace: true })
      }
    }
    fetchUser()
  }, [navigate])

  /** 根据 URL 的 post 参数加载帖子并填充表单 */
  useEffect(() => {
    if (!postIdParam || !userInfo) return
    const postId = Number(postIdParam)
    if (!postId) return

    const fetchPost = async () => {
      setLoading(true)
      try {
        const data = await getPostById(postId)
        setPost(data)
        setTitle(data.title || '')
        setStopLoss(String(data.stop_loss ?? ''))
        setTakeProfit(data.take_profit != null ? String(data.take_profit) : '')
        setDirection((data.direction as 'buy' | 'sell') || 'buy')
        setContent(data.content || '')
      } catch {
        navigate('/dashboard', { replace: true })
      } finally {
        setLoading(false)
      }
    }
    fetchPost()
  }, [postIdParam, userInfo, navigate])

  /** 权限：仅管理员可编辑 */
  useEffect(() => {
    if (!userInfo || !redirectChecked) return
    if (userInfo.user_role < 3) {
      navigate('/dashboard', { replace: true })
    }
  }, [userInfo, redirectChecked, navigate])

  const handleUpdatePost = async () => {
    if (!post) return
    if (!title.trim() || !content.trim() || stopLoss === '') {
      alert('请填写标题、止损价和内容')
      return
    }

    setUpdating(true)
    try {
      await updatePost(post.post_id, {
        title: title.trim(),
        contract_code: post.contract_code,
        stop_loss: parseFloat(stopLoss),
        take_profit: takeProfit ? parseFloat(takeProfit) : undefined,
        direction,
        content: content.trim(),
        suggestion: content.slice(0, 120),
        /* 现价不传，由后端定时任务更新 */
      })
      setPost(prev => prev ? { ...prev, title: title.trim(), stop_loss: parseFloat(stopLoss), take_profit: takeProfit ? parseFloat(takeProfit) : undefined, direction, content: content.trim() } : null)
      alert('帖子已更新')
    } catch (err) {
      console.error('[AdminPublish] 更新帖子失败', err)
      alert('更新失败，请稍后重试')
    } finally {
      setUpdating(false)
    }
  }

  const handleDeletePost = async () => {
    if (!post) return
    if (!confirm('确定删除该帖子吗？删除后将无法恢复。')) return

    setDeleting(true)
    try {
      await deletePost(post.post_id)
      alert('帖子已删除')
      navigate('/dashboard')
    } catch (err) {
      console.error('[AdminPublish] 删除帖子失败', err)
      alert('删除失败，请稍后重试')
    } finally {
      setDeleting(false)
    }
  }

  const goToDetail = () => {
    if (post) navigate(`/signal/${post.post_id}`)
  }

  if (!redirectChecked || !userInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
          <p className="mt-4 text-gray-500 font-medium">加载中...</p>
        </div>
      </div>
    )
  }

  if (!postIdParam) {
    return null
  }

  if (loading || !post) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
          <p className="mt-4 text-gray-500 font-medium">加载帖子...</p>
        </div>
      </div>
    )
  }

  return (
    <MainLayout user={userInfo} onLogout={() => {}}>
      <div className="grid grid-cols-12 gap-6 max-w-7xl mx-auto h-[calc(100vh-8rem)]">
        {/* 左侧：与详情页一致的结构 + 可编辑字段 */}
        <div className="col-span-9 bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-full">
          {/* 头部：合约、标题、现价（只读）、止损/止盈（可编辑） */}
          <div className="p-6 border-b border-gray-100">
            <div className="flex items-center gap-3 mb-3">
              <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded">
                {getContractName(post.contract_code)}
              </span>
              <span className="text-sm text-gray-500">{post.contract_code}</span>
            </div>

            <div className="mb-4">
              <label className="block text-xs text-gray-500 mb-1">标题</label>
              <input
                type="text"
                value={title}
                onChange={e => setTitle(e.target.value)}
                className="w-full text-2xl font-bold text-gray-900 px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                placeholder="帖子标题"
              />
            </div>

            <div className="flex flex-wrap gap-4 items-center">
              {/* 现价：只读展示，不可修改 */}
              <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-lg border border-blue-100">
                <span className="text-xs text-blue-500">现价</span>
                <span className="font-mono font-bold text-blue-700">
                  {post.current_price != null ? post.current_price.toLocaleString() : '—'}
                </span>
                <span className="text-xs text-gray-400">（由系统更新，不可修改）</span>
              </div>
              <div className="flex items-center gap-2 px-4 py-2 bg-red-50 rounded-lg border border-red-100">
                <span className="text-xs text-red-500">止损参考</span>
                <input
                  type="number"
                  value={stopLoss}
                  onChange={e => setStopLoss(e.target.value)}
                  className="font-mono font-bold text-red-700 w-24 bg-transparent border-b border-red-200 focus:outline-none focus:border-red-400"
                />
              </div>
              <div className="flex items-center gap-2 px-4 py-2 bg-green-50 rounded-lg border border-green-100">
                <span className="text-xs text-green-500">止盈参考</span>
                <input
                  type="number"
                  value={takeProfit}
                  onChange={e => setTakeProfit(e.target.value)}
                  className="font-mono font-bold text-green-700 w-24 bg-transparent border-b border-green-200 focus:outline-none focus:border-green-400"
                  placeholder="可选"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500 mr-2">方向</label>
                <select
                  value={direction}
                  onChange={e => setDirection(e.target.value as 'buy' | 'sell')}
                  className="px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                >
                  <option value="buy">做多</option>
                  <option value="sell">做空</option>
                </select>
              </div>
            </div>
          </div>

          {/* 可滚动区域：K 线图 + 正文编辑 */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* 日线 K 线图（与详情页一致） */}
            <div className="w-full bg-white rounded-xl border-2 border-gray-200 p-4 mb-6">
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                {post.contract_code} 历史 K 线图
              </h3>
              {post.contract_code ? (
                <KlineChart contractCode={post.contract_code} height={400} period={365} />
              ) : (
                <div className="w-full h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200 flex items-center justify-center text-gray-400">
                  暂无合约代码
                </div>
              )}
            </div>

            {/* 正文编辑 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">内容正文</label>
              <textarea
                value={content}
                onChange={e => setContent(e.target.value)}
                className="w-full min-h-[200px] p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none resize-y"
                placeholder="在此输入详细分析和建议..."
              />
            </div>
          </div>

          {/* 底部操作 */}
          <div className="p-4 border-t border-gray-100 bg-gray-50 flex justify-between items-center">
            <button
              type="button"
              onClick={goToDetail}
              className="px-4 py-2 text-gray-500 hover:bg-gray-200 rounded-lg transition-colors text-sm"
            >
              ← 返回详情
            </button>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={handleUpdatePost}
                disabled={updating}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 text-sm font-medium"
              >
                {updating ? '更新中...' : '更新帖子'}
              </button>
              <button
                type="button"
                onClick={handleDeletePost}
                disabled={deleting}
                className="px-4 py-2 text-red-500 hover:bg-red-50 rounded-lg border border-red-200 disabled:opacity-50 text-sm"
              >
                {deleting ? '删除中...' : '删除帖子'}
              </button>
            </div>
          </div>
        </div>

        {/* 右侧：操作说明（可选） */}
        <div className="col-span-3">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-bold text-gray-800 mb-2">编辑说明</h3>
            <p className="text-sm text-gray-500">
              可修改标题、止损参考、止盈参考、方向与正文。现价由系统定时更新，不可在此修改。
            </p>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}
