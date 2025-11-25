import { useNavigate, useLocation } from 'react-router-dom'

interface SidebarItem {
  name: string
  path: string
  adminOnly?: boolean
}

interface SidebarProps {
  user?: any
}

export default function Sidebar({ user }: SidebarProps) {
  const navigate = useNavigate()
  const location = useLocation()
  
  // 检查是否为管理员 (user_role >= 3)
  const isAdmin = user?.user_role >= 3 

  const items: SidebarItem[] = [
    { name: '发布', path: '/admin/publish', adminOnly: true },
    { name: '主页', path: '/dashboard' },
    { name: '搜索合约', path: '/search' },
    { name: '查看账户', path: '/account' },
  ]

  return (
    <aside className="w-64 bg-white border-r border-gray-200 h-screen fixed left-0 top-0 flex flex-col shadow-sm z-20 pt-20">
      <nav className="flex-1 py-6 px-4 space-y-2">
        {items.map((item) => {
          if (item.adminOnly && !isAdmin) return null
          
          const isActive = location.pathname === item.path || (item.path === '/dashboard' && location.pathname === '/')
          
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full text-left px-6 py-4 rounded-xl transition-all duration-200 font-medium text-lg ${
                isActive 
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-200' 
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
              }`}
            >
              {item.name}
            </button>
          )
        })}
      </nav>
    </aside>
  )
}
