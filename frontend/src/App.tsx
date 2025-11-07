/** 应用主组件。

这是应用的根组件，负责路由配置和全局状态管理。
*/

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { isAuthenticated } from './services/authService'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import './App.css'

/** 是否为开发模式。 */
const isDevMode = (import.meta as any).env?.MODE === 'development' || 
                  (import.meta as any).env?.VITE_DEV_MODE === 'true'

/**
 * 受保护的路由组件。
 * 
 * 如果用户未登录，重定向到登录页。
 * 开发模式下可以跳过认证检查。
 * 
 * @param children - 子组件。
 * @returns JSX 元素。
 */
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  // 开发模式下跳过认证检查
  if (isDevMode) {
    return <>{children}</>
  }
  
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

/**
 * 应用主组件。
 * 
 * @returns JSX 元素。
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 登录页 */}
        <Route path="/login" element={<Login />} />
        
        {/* 注册页 */}
        <Route path="/register" element={<Register />} />
        
        {/* 仪表板（受保护） */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        
        {/* 默认重定向到仪表板 */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        
        {/* 404 页面 */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
