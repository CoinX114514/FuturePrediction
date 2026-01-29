import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5175,
    strictPort: false, // 如果端口被占用，尝试其他端口
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        timeout: 30000, // 30秒超时
        proxyTimeout: 30000, // 代理超时时间
      },
    },
    hmr: {
      host: 'localhost',
      port: 5175,
      timeout: 10000, // HMR 超时设置
    },
    cors: true, // 启用 CORS
  },
})

