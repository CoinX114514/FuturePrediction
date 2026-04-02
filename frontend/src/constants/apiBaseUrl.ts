/** 后端 API 根路径（axios baseURL）。

设计原因：生产构建若未注入 VITE_API_BASE_URL，旧逻辑会回退到 http://localhost:8000，
浏览器访问线上页面时请求打到用户本机，导致超时或 502。默认使用相对路径 `/api`，
与同域 Nginx 反代一致；仅在前后端分离部署时再设置环境变量为完整 URL。
 */
export const API_BASE_URL =
  (import.meta.env as { VITE_API_BASE_URL?: string }).VITE_API_BASE_URL || '/api'
