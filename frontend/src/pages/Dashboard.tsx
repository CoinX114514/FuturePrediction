/** 交易仪表板页面组件。

主界面，包含实时行情、板块榜单、AI预测面板、基础信息等模块。
*/

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import FileUpload, { OHLCVData } from '../components/FileUpload'
import KLineChart from '../components/KLineChart'
import Rankings from '../components/Rankings'
import MarketData from '../components/MarketData'
import ContractInfo from '../components/ContractInfo'
import { logout, getCurrentUser } from '../services/authService'

/**
 * 交易仪表板页面组件。
 * 
 * @returns JSX 元素。
 */
export default function Dashboard() {
  /** 导航钩子。 */
  const navigate = useNavigate()
  
  /** 当前上传的文件 ID。 */
  const [fileId, setFileId] = useState<string | null>(null)
  
  /** 上传的CSV数据。 */
  const [csvData, setCsvData] = useState<OHLCVData[] | null>(null)
  
  /** 加载状态。 */
  const [loading, setLoading] = useState<boolean>(false)
  
  /** 错误信息。 */
  const [error, setError] = useState<string | null>(null)
  
  /** 用户信息。 */
  const [userInfo, setUserInfo] = useState<any>(null)


  /** 是否为开发模式。 */
  const isDevMode = (import.meta as any).env?.MODE === 'development' || 
                    (import.meta as any).env?.VITE_DEV_MODE === 'true'

  /**
   * 组件挂载时获取用户信息。
   */
  useEffect(() => {
    const fetchUserInfo = async () => {
      // 开发模式下使用 mock 用户信息
      if (isDevMode) {
        setUserInfo({
          user_id: 1,
          phone_number: '13800138000',
          nickname: '开发模式用户',
          user_role: 2, // 会员
        })
        return
      }

      try {
        const user = await getCurrentUser()
        setUserInfo(user)
      } catch (err) {
        navigate('/login')
      }
    }
    fetchUserInfo()
  }, [navigate, isDevMode])

  /**
   * 处理文件上传成功回调。
   * 
   * @param uploadedFileId - 上传成功后的文件 ID。
   * @param data - 解析后的CSV数据。
   */
  const handleUploadSuccess = (uploadedFileId: string, data: OHLCVData[]) => {
    setFileId(uploadedFileId)
    setCsvData(data)
    setError(null)
  }

  /**
   * 处理文件上传错误。
   * 
   * @param errorMessage - 错误消息。
   */
  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage)
    setFileId(null)
    setCsvData(null)
  }

  /**
   * 设置加载状态。
   * 
   * @param isLoading - 是否正在加载。
   */
  const setLoadingState = (isLoading: boolean) => {
    setLoading(isLoading)
  }

  /**
   * 处理登出。
   */
  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  if (!userInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    )
  }

  const isMember = userInfo.user_role >= 2

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* 导航栏 */}
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold text-gray-800">期货价格趋势预测</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {userInfo.nickname || userInfo.phone_number}
                {isMember && (
                  <span className="ml-2 px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs">
                    会员
                  </span>
                )}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
              >
                登出
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-6">
        {/* 错误提示 */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <p className="font-medium">错误：</p>
            <p>{error}</p>
          </div>
        )}

        {/* 主要内容区域 - 网格布局 */}
        <div className="grid grid-cols-12 gap-6">
          {/* 左侧列 - K线图、上传和实时行情 */}
          <div className="col-span-12 lg:col-span-8 space-y-6">
            {/* K线图 */}
            <KLineChart 
              contractCode="IF2312"
              csvData={csvData || undefined}
              fileId={fileId}
              onLoadingChange={setLoadingState}
            />

            {/* CSV上传 */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <FileUpload
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
                disabled={loading}
              />
            </div>

            {/* 实时行情模块（仅在未上传CSV时显示） */}
            {!csvData && (
              <MarketData contractCode="IF2312" />
            )}
          </div>

          {/* 右侧列 - 板块榜单和基础信息 */}
          <div className="col-span-12 lg:col-span-4 space-y-6">
            {/* 板块榜单 */}
            <Rankings isMember={isMember} />

            {/* 基础信息栏（仅在未上传CSV时显示） */}
            {!csvData && (
              <ContractInfo contractCode="IF2312" />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
