import { useState, useEffect } from 'react'
import MainLayout from '../components/layout/MainLayout'
import { useNavigate } from 'react-router-dom'
import { getCurrentUser } from '../services/authService'
import { getCollections, getBrowseHistory, getUserPosts, getDrafts, PostItem } from '../services/accountService'
import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser,
  AdminUser,
  AdminUserPayload
} from '../services/adminUserService'

type AdminFormState = {
  phone_number: string
  password: string
  email: string
  nickname: string
  user_role: number
  is_active: boolean
  daily_prediction_limit?: number
}

export default function Account() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'favorites' | 'history' | 'posts' | 'drafts' | 'adminUsers'>('favorites')
  
  /** 用户信息状态。从后端获取真实数据。 */
  const [userInfo, setUserInfo] = useState<any>(null)
  
  /** 列表数据状态。 */
  const [items, setItems] = useState<any[]>([])
  /** 管理员用户列表 */
  const [adminUsers, setAdminUsers] = useState<AdminUser[]>([])
  const [adminTotal, setAdminTotal] = useState(0)
  const [adminPage, setAdminPage] = useState(1)
  const [adminPageSize] = useState(10)
  const [adminLoading, setAdminLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const [editUser, setEditUser] = useState<AdminUser | null>(null)
  const [form, setForm] = useState<AdminFormState>({
    phone_number: '',
    password: '',
    email: '',
    nickname: '',
    user_role: 1,
    is_active: true,
    daily_prediction_limit: 5,
  })
  
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
          case 'adminUsers':
            // 管理员分页拉取用户
            setAdminLoading(true)
            const res = await fetchUsers(adminPage, adminPageSize)
            setAdminUsers(res.users)
            setAdminTotal(res.total)
            setAdminLoading(false)
            data = []
            break
        }
        
        setItems(data)
      } catch (err) {
        console.error(`[Account] 获取${activeTab}数据失败`, err)
        setItems([])
        if (activeTab === 'adminUsers') {
          setAdminUsers([])
          setAdminTotal(0)
        }
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [activeTab, userInfo, adminPage, adminPageSize])

  const handleEdit = (user: AdminUser) => {
    setErrorMsg(null)
    setEditUser(user)
    setForm({
      phone_number: user.phone_number,
      password: '',
      email: user.email || '',
      nickname: user.nickname || '',
      user_role: user.user_role,
      is_active: user.is_active,
      daily_prediction_limit: user.daily_prediction_limit ?? 5,
    })
  }

  const resetForm = () => {
    setErrorMsg(null)
    setEditUser(null)
    setForm({
      phone_number: '',
      password: '',
      email: '',
      nickname: '',
      user_role: 1,
      is_active: true,
      daily_prediction_limit: 5,
    })
  }

  const submitUser = async () => {
    setErrorMsg(null)
    // 基础校验
    const phone = form.phone_number.trim()
    const email = form.email?.trim() || ''
    const nickname = form.nickname?.trim() || ''
    const pwd = form.password?.trim() || ''

    if (!editUser) {
      if (!phone) return setErrorMsg('手机号不能为空')
      if (!/^[0-9]{11}$/.test(phone)) return setErrorMsg('手机号需为11位数字')
      if (!pwd || pwd.length < 6) return setErrorMsg('密码至少6位')
    }

    const payload: AdminUserPayload = {}
    if (!editUser || phone !== editUser.phone_number) payload.phone_number = phone
    if (email !== (editUser?.email || '')) payload.email = email || undefined
    if (nickname !== (editUser?.nickname || '')) payload.nickname = nickname || undefined
    if (pwd) payload.password = pwd
    if (form.user_role !== undefined) payload.user_role = form.user_role
    if (form.is_active !== undefined) payload.is_active = form.is_active
    if (Number.isFinite(form.daily_prediction_limit)) payload.daily_prediction_limit = Number(form.daily_prediction_limit)

    try {
      setSaving(true)
      if (editUser) {
        await updateUser(editUser.user_id, payload)
      } else {
        const createPayload: AdminUserPayload = {
          phone_number: phone,
          password: pwd,
          email: email || undefined,
          nickname: nickname || undefined,
          user_role: form.user_role,
          is_active: form.is_active,
          daily_prediction_limit: Number.isFinite(form.daily_prediction_limit)
            ? Number(form.daily_prediction_limit)
            : 5,
        }
        await createUser(createPayload)
      }
      resetForm()
      const res = await fetchUsers(adminPage, adminPageSize)
      setAdminUsers(res.users)
      setAdminTotal(res.total)
    } catch (err: any) {
      setErrorMsg(err?.response?.data?.detail || err?.message || '操作失败')
    } finally {
      setSaving(false)
    }
  }

  const removeUser = async (userId: number) => {
    if (!window.confirm('确认删除该用户？')) return
    await deleteUser(userId)
    const res = await fetchUsers(adminPage, adminPageSize)
    setAdminUsers(res.users)
    setAdminTotal(res.total)
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
                { id: 'drafts', label: '草稿箱' },
                ...(userInfo?.user_role === 3 ? [{ id: 'adminUsers', label: '用户管理' }] : []),
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

           {/* Content */}
           <div className="p-4">
              {activeTab === 'adminUsers' ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <input className="input input-bordered w-full" placeholder="手机号" value={form.phone_number} onChange={e => setForm({ ...form, phone_number: e.target.value })} />
                    <input className="input input-bordered w-full" placeholder="邮箱" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
                    <input className="input input-bordered w-full" placeholder="昵称" value={form.nickname} onChange={e => setForm({ ...form, nickname: e.target.value })} />
                    <input className="input input-bordered w-full" placeholder="密码（留空则不改）" type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
                    <input className="input input-bordered w-full" placeholder="每日预测上限" type="number" value={form.daily_prediction_limit ?? 5} onChange={e => setForm({ ...form, daily_prediction_limit: Number(e.target.value) })} />
                    <select className="select select-bordered w-full" value={form.user_role} onChange={e => setForm({ ...form, user_role: Number(e.target.value) })}>
                      <option value={1}>普通用户</option>
                      <option value={2}>VIP会员</option>
                      <option value={3}>超级管理员</option>
                    </select>
                    <label className="flex items-center gap-2 text-sm text-gray-600">
                      <input type="checkbox" checked={form.is_active} onChange={e => setForm({ ...form, is_active: e.target.checked })} />
                      账户激活
                    </label>
                  </div>
                  {errorMsg && <div className="text-sm text-red-600">{errorMsg}</div>}
                  <div className="flex gap-2">
                    <button className="btn btn-primary" disabled={saving} onClick={submitUser}>
                      {saving ? '保存中...' : editUser ? '保存修改' : '新增用户'}
                    </button>
                    {editUser && (
                      <button className="btn btn-ghost" onClick={resetForm} disabled={saving}>
                        放弃编辑
                      </button>
                    )}
                  </div>
                  <div className="overflow-auto border rounded-xl">
                    <table className="min-w-full text-sm">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-3 py-2 text-left">ID</th>
                          <th className="px-3 py-2 text-left">手机号</th>
                          <th className="px-3 py-2 text-left">邮箱</th>
                          <th className="px-3 py-2 text-left">昵称</th>
                          <th className="px-3 py-2 text-left">角色</th>
                          <th className="px-3 py-2 text-left">状态</th>
                          <th className="px-3 py-2 text-left">创建时间</th>
                          <th className="px-3 py-2 text-left">操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        {adminLoading ? (
                          <tr><td colSpan={8} className="text-center py-4 text-gray-500">加载中...</td></tr>
                        ) : adminUsers.length === 0 ? (
                          <tr><td colSpan={8} className="text-center py-4 text-gray-400">暂无用户</td></tr>
                        ) : (
                          adminUsers.map(u => (
                            <tr key={u.user_id} className="border-t">
                              <td className="px-3 py-2">{u.user_id}</td>
                              <td className="px-3 py-2">{u.phone_number}</td>
                              <td className="px-3 py-2">{u.email || '-'}</td>
                              <td className="px-3 py-2">{u.nickname || '-'}</td>
                              <td className="px-3 py-2">{getRoleName(u.user_role)}</td>
                              <td className="px-3 py-2">{u.is_active ? '启用' : '禁用'}</td>
                              <td className="px-3 py-2">{u.created_at ? new Date(u.created_at).toLocaleString('zh-CN') : '-'}</td>
                              <td className="px-3 py-2 space-x-2">
                                <button className="text-blue-600" onClick={() => handleEdit(u)}>编辑</button>
                                <button className="text-red-600" onClick={() => removeUser(u.user_id)}>删除</button>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span>共 {adminTotal} 条</span>
                    <div className="space-x-2">
                      <button className="btn" disabled={adminPage === 1} onClick={() => setAdminPage(p => Math.max(1, p - 1))}>上一页</button>
                      <button className="btn" disabled={adminPage * adminPageSize >= adminTotal} onClick={() => setAdminPage(p => p + 1)}>下一页</button>
                    </div>
                  </div>
                </div>
              ) : (
                <>
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
                </>
              )}
           </div>
        </div>
      </div>
    </MainLayout>
  )
}

