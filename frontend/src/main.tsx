import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// 简单的错误边界组件
class ErrorBoundary extends React.Component<{ children: React.ReactNode }, { hasError: boolean, error: Error | null }> {
  constructor(props: { children: React.ReactNode }) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
          <h1>Something went wrong.</h1>
          <p>请查看控制台获取详细错误信息。</p>
          <pre style={{ color: 'red', background: '#eee', padding: '10px' }}>
            {this.state.error?.toString()}
          </pre>
        </div>
      )
    }

    return this.props.children
  }
}

console.log("[main.tsx] 开始挂载 React 根组件...")
const startTime = Date.now()

// 检查 root 元素是否存在
const rootElement = document.getElementById('root')
if (!rootElement) {
  console.error("[main.tsx] 错误: 找不到 #root 元素！")
  document.body.innerHTML = '<div style="padding: 20px; color: red;">错误: 找不到 #root 元素</div>'
} else {
  console.log("[main.tsx] 找到 #root 元素，开始渲染...")
  
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </React.StrictMode>,
  )
  
  const elapsed = Date.now() - startTime
  console.log(`[main.tsx] React 根组件挂载完成，耗时: ${elapsed}ms`)
}
