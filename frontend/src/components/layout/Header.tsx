interface HeaderProps {
  user: any
  onLogout?: () => void
}

export default function Header({ user }: HeaderProps) {
  return (
    <header className="h-16 bg-blue-600 flex items-center justify-between px-8 fixed top-0 right-0 left-0 z-30 shadow-md">
      {/* Left: Logo/System Name */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center text-blue-600 font-bold text-xl">
          Q
        </div>
        <h1 className="text-xl font-bold text-white tracking-wide">
          XX期货预测系统
        </h1>
      </div>

      {/* Right: User Info */}
      <div className="flex items-center gap-6 text-white/90 text-sm font-medium">
        <div className="flex items-center gap-4 bg-blue-700/50 px-4 py-2 rounded-full border border-blue-500/30">
          <span className="flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            {user?.nickname || '用户'}
          </span>
          <span className="w-px h-4 bg-blue-400/50"></span>
          <span className="text-green-300">状态: 在线</span>
          <span className="w-px h-4 bg-blue-400/50"></span>
          <span className="text-yellow-300">等级: {user?.user_role >= 2 ? 'VIP会员' : '普通用户'}</span>
          {user?.user_role >= 2 && (
            <>
              <span className="w-px h-4 bg-blue-400/50"></span>
              <span className="text-gray-200">VIP到期: 2025-12-31</span>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
