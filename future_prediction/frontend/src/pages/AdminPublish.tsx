import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'
import { getCurrentUser } from '../services/authService'
import { DraftSummary, getDrafts, getDraftById, createDraft, updateDraft, deleteDraft } from '../services/draftService'
import { getUserPosts } from '../services/accountService'
import { createPost, updatePost, deletePost, getPostById, Post } from '../services/postService'

export default function AdminPublish() {
  const [title, setTitle] = useState('')
  const [contractCode, setContractCode] = useState('')
  const [stopLoss, setStopLoss] = useState('')
  const [takeProfit, setTakeProfit] = useState('')
  const [content, setContent] = useState('')
  const [currentDraftId, setCurrentDraftId] = useState<number | null>(null)
  const [currentPostId, setCurrentPostId] = useState<number | null>(null)
  const [drafts, setDrafts] = useState<DraftSummary[]>([])
  const [myPosts, setMyPosts] = useState<Post[]>([])
  const [loadingDrafts, setLoadingDrafts] = useState(false)
  const [loadingPosts, setLoadingPosts] = useState(false)
  const [saving, setSaving] = useState(false)
  const [publishing, setPublishing] = useState(false)
  const [deletingDraft, setDeletingDraft] = useState(false)
  const [updatingPost, setUpdatingPost] = useState(false)
  const [deletingPostFlag, setDeletingPostFlag] = useState(false)
  
  /** 用户信息状态。从后端获取真实数据。 */
  const [userInfo, setUserInfo] = useState<any>(null)
  const [searchParams, setSearchParams] = useSearchParams()
  const [initialQueryHandled, setInitialQueryHandled] = useState(false)

  const resetForm = () => {
    setTitle('')
    setContractCode('')
    setStopLoss('')
    setTakeProfit('')
    setContent('')
    setCurrentDraftId(null)
    setCurrentPostId(null)
  }

  const refreshDrafts = async () => {
    setLoadingDrafts(true)
    try {
      const data = await getDrafts()
      setDrafts(data)
    } catch (err) {
      console.error('[AdminPublish] 获取草稿列表失败', err)
      setDrafts([])
    } finally {
      setLoadingDrafts(false)
    }
  }

  const refreshPosts = async () => {
    setLoadingPosts(true)
    try {
      const response = await getUserPosts(1, 50)
      setMyPosts(response.posts || [])
    } catch (err) {
      console.error('[AdminPublish] 获取已发布帖子失败', err)
      setMyPosts([])
    } finally {
      setLoadingPosts(false)
    }
  }

  const clearQueryParams = () => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev)
      next.delete('draft')
      next.delete('post')
      return next
    }, { replace: true })
  }

  /** 从后端获取用户信息 & 草稿列表。 */
  useEffect(() => {
    const fetchData = async () => {
      try {
        const user = await getCurrentUser()
        setUserInfo(user)
        await Promise.all([refreshDrafts(), refreshPosts()])
      } catch (err) {
        console.error('[AdminPublish] 初始化失败', err)
      }
    }
    if (!userInfo) {
      fetchData()
    }
  }, [userInfo])

  useEffect(() => {
    if (!userInfo || initialQueryHandled) return
    const draftParam = searchParams.get('draft')
    const postParam = searchParams.get('post')

    if (draftParam) {
      handleSelectDraft(Number(draftParam))
      clearQueryParams()
      setInitialQueryHandled(true)
      return
    }

    if (postParam) {
      handleSelectPost(Number(postParam))
      clearQueryParams()
      setInitialQueryHandled(true)
      return
    }

    setInitialQueryHandled(true)
  }, [userInfo, searchParams, initialQueryHandled])

  const handleSelectDraft = async (draftId: number) => {
    try {
      const draft = await getDraftById(draftId)
      setCurrentDraftId(draft.draft_id)
      setCurrentPostId(null)
      setTitle(draft.title || '')
      setContractCode(draft.contract_code || '')
      setStopLoss(draft.stop_loss?.toString() || '')
      setTakeProfit(draft.take_profit?.toString() || '')
      setContent(draft.content || '')
    } catch (err) {
      console.error('[AdminPublish] 获取草稿详情失败', err)
    }
  }

  const handleSelectPost = async (postId: number) => {
    try {
      const post = await getPostById(postId)
      setCurrentPostId(post.post_id)
      setCurrentDraftId(null)
      setTitle(post.title || '')
      setContractCode(post.contract_code || '')
      setStopLoss(post.stop_loss?.toString() || '')
      setTakeProfit(post.take_profit?.toString() || '')
      setContent(post.content || '')
    } catch (err) {
      console.error('[AdminPublish] 获取帖子详情失败', err)
    }
  }

  const handleSaveDraft = async () => {
    if (!title || !contractCode || !stopLoss || !content) {
      alert('请至少填写标题、合约代码、止损价和内容后再保存草稿')
      return
    }

    const payload = {
      title,
      contract_code: contractCode,
      stop_loss: parseFloat(stopLoss),
      take_profit: takeProfit ? parseFloat(takeProfit) : undefined,
      content,
    }

    setSaving(true)
    try {
      let draft
      if (currentDraftId) {
        draft = await updateDraft(currentDraftId, payload)
      } else {
        draft = await createDraft(payload)
      }
      await refreshDrafts()
      setCurrentDraftId(draft.draft_id)
      setCurrentPostId(null)
      alert('草稿保存成功')
    } catch (err) {
      console.error('[AdminPublish] 保存草稿失败', err)
      alert('保存草稿失败，请稍后重试')
    } finally {
      setSaving(false)
    }
  }

  const handleDeleteDraft = async () => {
    if (!currentDraftId) {
      alert('请先选择一个草稿')
      return
    }
    if (!confirm('确定删除当前草稿吗？')) return

    setDeletingDraft(true)
    try {
      await deleteDraft(currentDraftId)
      await refreshDrafts()
      resetForm()
      alert('草稿已删除')
    } catch (err) {
      console.error('[AdminPublish] 删除草稿失败', err)
      alert('删除草稿失败，请稍后重试')
    } finally {
      setDeletingDraft(false)
    }
  }

  const handlePublish = async () => {
    if (!userInfo || userInfo.user_role < 3) {
      alert('只有管理员可以发布帖子')
      return
    }
    if (!title || !contractCode || !stopLoss || !content) {
      alert('请完整填写标题、合约代码、止损价和内容')
      return
    }

    setPublishing(true)
    try {
      await createPost({
        title,
        contract_code: contractCode,
        stop_loss: parseFloat(stopLoss),
        take_profit: takeProfit ? parseFloat(takeProfit) : undefined,
        content,
        suggestion: content.slice(0, 120),
      })
      if (currentDraftId) {
        await deleteDraft(currentDraftId)
      }
      await refreshDrafts()
      resetForm()
      alert('发布成功')
    } catch (err) {
      console.error('[AdminPublish] 发布失败', err)
      alert('发布失败，请稍后再试')
    } finally {
      setPublishing(false)
    }
  }

  const handleUpdatePost = async () => {
    if (!currentPostId) {
      alert('请先选择一个要编辑的帖子')
      return
    }
    if (!title || !contractCode || !stopLoss || !content) {
      alert('请完整填写标题、合约代码、止损价和内容')
      return
    }

    setUpdatingPost(true)
    try {
      await updatePost(currentPostId, {
        title,
        contract_code: contractCode,
        stop_loss: parseFloat(stopLoss),
        take_profit: takeProfit ? parseFloat(takeProfit) : undefined,
        content,
        suggestion: content.slice(0, 120),
      })
      await refreshPosts()
      alert('帖子已更新')
    } catch (err) {
      console.error('[AdminPublish] 更新帖子失败', err)
      alert('更新失败，请稍后再试')
    } finally {
      setUpdatingPost(false)
    }
  }

  const handleDeletePost = async () => {
    if (!currentPostId) {
      alert('请先选择一个帖子')
      return
    }
    if (!confirm('确定删除该帖子吗？删除后将无法恢复。')) return

    setDeletingPostFlag(true)
    try {
      await deletePost(currentPostId)
      await refreshPosts()
      resetForm()
      alert('帖子已删除')
    } catch (err) {
      console.error('[AdminPublish] 删除帖子失败', err)
      alert('删除失败，请稍后再试')
    } finally {
      setDeletingPostFlag(false)
    }
  }

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

  if (userInfo.user_role < 3) {
    return (
      <MainLayout user={userInfo} onLogout={() => {}}>
        <div className="min-h-[60vh] flex items-center justify-center">
          <div className="bg-white shadow-sm border border-gray-200 rounded-2xl p-10 text-center max-w-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">权限不足</h2>
            <p className="text-gray-500">只有管理员可以访问发布中心。</p>
          </div>
        </div>
      </MainLayout>
    )
  }

  return (
    <MainLayout user={userInfo} onLogout={() => {}}>
      <div className="grid grid-cols-12 gap-6 h-[calc(100vh-8rem)]">
        {/* Left Column: Inputs & Editor */}
        <div className="col-span-9 flex flex-col gap-4 h-full overflow-y-auto pr-2">
          {/* Header Info */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 space-y-4">
            <div className="flex gap-4">
               <div className="flex-1">
                 <label className="block text-sm font-medium text-gray-700 mb-1">信息标题</label>
                 <input 
                   type="text" 
                   value={title}
                   onChange={(e) => setTitle(e.target.value)}
                   className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                   placeholder="请输入标题..."
                 />
               </div>
            </div>
            
            <div className="grid grid-cols-3 gap-4">
               <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">目标合约代码</label>
                 <div className="relative">
                    <input 
                      type="text" 
                      value={contractCode}
                      onChange={(e) => setContractCode(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                      placeholder="搜索合约 (e.g. IF2312)"
                    />
                    <button className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-600">
                       <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </button>
                 </div>
               </div>
               <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">止损价</label>
                 <input 
                   type="number" 
                   value={stopLoss}
                   onChange={(e) => setStopLoss(e.target.value)}
                   className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                   placeholder="0.00"
                 />
               </div>
               <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">止盈价 (可选)</label>
                 <input 
                   type="number" 
                   value={takeProfit}
                   onChange={(e) => setTakeProfit(e.target.value)}
                   className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                   placeholder="0.00"
                 />
               </div>
            </div>
          </div>

          {/* Content Editor & Chart Placeholder */}
          <div className="flex-1 flex gap-4 min-h-[500px]">
             {/* Text Editor */}
             <div className="w-1/2 bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col">
                <label className="text-sm font-medium text-gray-700 mb-2">内容正文录入</label>
                <textarea 
                   value={content}
                   onChange={(e) => setContent(e.target.value)}
                   className="flex-1 w-full p-4 bg-gray-50 border border-gray-200 rounded-lg resize-none focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                   placeholder="在此输入详细分析和建议..."
                />
             </div>

             {/* Chart Placeholder */}
             <div className="w-1/2 bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col">
                <label className="text-sm font-medium text-gray-700 mb-2">合约 K 线图展示 (如有)</label>
                <div className="flex-1 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                   <div className="text-center text-gray-400">
                      <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
                      <p>K 线图表区域</p>
                      <p className="text-xs mt-1">输入合约代码后自动加载</p>
                   </div>
                </div>
             </div>
          </div>
        </div>

        {/* Right Column: Actions & Drafts */}
        <div className="col-span-3 flex flex-col gap-4">
          {/* Action Buttons */}
          <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 space-y-3">
             <button
               onClick={currentPostId ? handleUpdatePost : handlePublish}
               disabled={currentPostId ? updatingPost : publishing}
               className="w-full py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors shadow-sm disabled:opacity-50"
             >
               {currentPostId
                 ? (updatingPost ? '更新中...' : '更新帖子')
                 : (publishing ? '发布中...' : '发布')}
             </button>
             <button
               onClick={handleSaveDraft}
               disabled={saving}
               className="w-full py-2.5 bg-white border border-blue-200 text-blue-600 rounded-lg hover:bg-blue-50 font-medium transition-colors disabled:opacity-50"
             >
                {saving ? '保存草稿中...' : '保存草稿'}
             </button>
             <div className="h-px bg-gray-100 my-2"></div>
             <button
               onClick={currentDraftId ? handleDeleteDraft : handleDeletePost}
               disabled={
                 (currentDraftId ? deletingDraft : deletingPostFlag) ||
                 (!currentDraftId && !currentPostId)
               }
               className="w-full py-2.5 text-red-500 hover:bg-red-50 rounded-lg text-sm transition-colors disabled:opacity-50"
             >
                {currentDraftId
                  ? (deletingDraft ? '删除草稿中...' : '删除草稿')
                  : (deletingPostFlag ? '删除帖子中...' : '删除帖子')}
             </button>
          </div>

           {/* Draft Box */}
           <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex-1 flex flex-col">
              <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                 <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                 草稿箱
              </h3>
              <div className="flex-1 overflow-y-auto space-y-2">
                 {loadingDrafts ? (
                   <div className="text-center text-gray-400 py-6 text-sm">草稿加载中...</div>
                 ) : drafts.length === 0 ? (
                   <div className="text-center text-gray-400 py-6 text-sm">暂无草稿</div>
                 ) : (
                   drafts.map((draft) => (
                     <button
                       key={draft.draft_id}
                       onClick={() => handleSelectDraft(draft.draft_id)}
                       className={`w-full text-left p-3 rounded-lg border transition-colors ${
                         draft.draft_id === currentDraftId
                           ? 'bg-blue-50 border-blue-200 text-blue-700'
                           : 'bg-gray-50 border-transparent hover:bg-blue-50 hover:border-blue-100'
                       }`}
                     >
                        <p className="text-sm font-medium truncate">{draft.title || '未命名草稿'}</p>
                        <p className="text-xs text-gray-400 mt-1">{new Date(draft.update_time).toLocaleString('zh-CN')}</p>
                     </button>
                   ))
                 )}
              </div>
           </div>

           {/* My Posts */}
           <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex-1 flex flex-col">
              <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                 <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                 我的已发布帖子
              </h3>
              <div className="flex-1 overflow-y-auto space-y-2">
                 {loadingPosts ? (
                   <div className="text-center text-gray-400 py-6 text-sm">加载中...</div>
                 ) : myPosts.length === 0 ? (
                   <div className="text-center text-gray-400 py-6 text-sm">暂无已发布帖子</div>
                 ) : (
                   myPosts.map((post) => (
                     <button
                       key={post.post_id}
                       onClick={() => handleSelectPost(post.post_id)}
                       className={`w-full text-left p-3 rounded-lg border transition-colors ${
                         post.post_id === currentPostId
                           ? 'bg-amber-50 border-amber-200 text-amber-700'
                           : 'bg-gray-50 border-transparent hover:bg-amber-50 hover:border-amber-100'
                       }`}
                     >
                        <p className="text-sm font-medium truncate">{post.title}</p>
                        <p className="text-xs text-gray-400 mt-1">{new Date(post.publish_time).toLocaleString('zh-CN')}</p>
                     </button>
                   ))
                 )}
              </div>
           </div>
        </div>
      </div>
    </MainLayout>
  )
}

