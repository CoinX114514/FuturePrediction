import { useState } from 'react'
import { predictTrend } from '../services/api'
import Chart from './Chart'

/** 预测结果组件的属性接口。 */
interface PredictionResultsProps {
  /** 文件 ID。 */
  fileId: string
  /** 预测成功回调函数。 */
  onPredictionSuccess: (data: any) => void
  /** 预测错误回调函数。 */
  onPredictionError: (error: string) => void
  /** 加载状态变化回调函数。 */
  onLoadingChange: (loading: boolean) => void
  /** 是否正在加载。 */
  loading: boolean
}

/** 预测结果组件。
 * 
 * 显示预测表单和结果。
 * 
 * @param props - 组件属性。
 */
function PredictionResults({
  fileId,
  onPredictionSuccess,
  onPredictionError,
  onLoadingChange,
  loading,
}: PredictionResultsProps) {
  /** 预测天数。 */
  const [days, setDays] = useState<number>(1)
  
  /** 预测结果数据。 */
  const [predictionData, setPredictionData] = useState<any>(null)

  /**
   * 执行预测。
   */
  const handlePredict = async () => {
    if (days < 1 || days > 30) {
      onPredictionError('预测天数必须在 1-30 天之间')
      return
    }

    onLoadingChange(true)

    try {
      const response = await predictTrend(fileId, days)
      setPredictionData(response)
      onPredictionSuccess(response)
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.detail || error.message || '预测失败'
      onPredictionError(errorMessage)
    } finally {
      onLoadingChange(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">执行预测</h2>
      
      <div className="space-y-4">
        {/* 预测参数设置 */}
        <div className="flex items-center gap-4">
          <label htmlFor="days" className="text-gray-700 font-medium">
            预测未来天数：
          </label>
          <input
            id="days"
            type="number"
            min="1"
            max="30"
            value={days}
            onChange={(e) => setDays(parseInt(e.target.value) || 1)}
            className="border border-gray-300 rounded-lg px-4 py-2 w-24 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={handlePredict}
            disabled={loading}
            className={`
              px-6 py-2 rounded-lg font-medium text-white
              transition-colors duration-200
              ${
                loading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }
            `}
          >
            {loading ? '预测中...' : '开始预测'}
          </button>
        </div>

        {/* 加载指示器 */}
        {loading && (
          <div className="flex items-center gap-2 text-blue-600">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <p>正在执行预测，请稍候...</p>
          </div>
        )}

        {/* 预测结果展示 */}
        {predictionData && !loading && (
          <div className="mt-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <p className="text-sm text-gray-600 mb-1">趋势方向</p>
                <p className="text-2xl font-bold text-blue-600">
                  {predictionData.trend}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <p className="text-sm text-gray-600 mb-1">置信度</p>
                <p className="text-2xl font-bold text-green-600">
                  {(predictionData.confidence * 100).toFixed(1)}%
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <p className="text-sm text-gray-600 mb-1">预测天数</p>
                <p className="text-2xl font-bold text-purple-600">
                  {predictionData.metadata?.prediction_days || days}
                </p>
              </div>
            </div>

            {/* 图表组件 */}
            {predictionData.predictions && (
              <div className="mt-6">
                <Chart
                  predictions={predictionData.predictions}
                  trend={predictionData.trend}
                />
              </div>
            )}

            {/* 详细预测值 */}
            {predictionData.predictions && (
              <div className="mt-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">
                  详细预测值
                </h3>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                    {predictionData.predictions.map(
                      (pred: number, index: number) => (
                        <div
                          key={index}
                          className="text-center p-2 bg-white rounded border"
                        >
                          <p className="text-xs text-gray-500">第 {index + 1} 天</p>
                          <p className="text-sm font-semibold text-gray-800">
                            {(pred * 100).toFixed(2)}%
                          </p>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default PredictionResults

