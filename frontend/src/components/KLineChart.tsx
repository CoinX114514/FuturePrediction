/** K线图组件。

显示期货合约的日线 K 线图，支持显示上传的CSV数据和预测结果。
*/

import { useState } from 'react'
import Chart from './Chart'
import CandlestickChart, { OHLCVData } from './CandlestickChart'

/** K线图组件的属性接口。 */
interface KLineChartProps {
  /** 合约代码。 */
  contractCode?: string
  /** 上传的CSV数据。 */
  csvData?: OHLCVData[]
  /** 文件ID（用于预测）。 */
  fileId?: string | null
  /** 加载状态变化回调。 */
  onLoadingChange?: (loading: boolean) => void
}

/**
 * K线图组件。
 * 
 * @param props - 组件属性。
 * @returns JSX 元素。
 */
export default function KLineChart({ 
  contractCode = 'IF2312',
  csvData,
  fileId,
  onLoadingChange
}: KLineChartProps) {
  /** 预测结果数据。 */
  const [predictionData, setPredictionData] = useState<any>(null)
  
  /** 预测按钮状态（模型未完成，默认可点击）。 */
  const predicting = false
  
  /** 预测错误信息。 */
  const [predictionError, setPredictionError] = useState<string | null>(null)
  
  /** 预测天数。 */
  const [predictionDays, setPredictionDays] = useState<number>(1)

  /** 模型建设中提示框。 */
  const [showModelDialog, setShowModelDialog] = useState(false)

  /** 是否有上传数据。 */
  const hasData = csvData && csvData.length > 0

  /**
   * 处理预测按钮点击。
   */
  const handlePredict = async () => {
    if (!fileId) {
      setPredictionError('请先上传CSV文件')
      return
    }

    if (predictionDays < 1 || predictionDays > 30) {
      setPredictionError('预测天数必须在 1-30 天之间')
      return
    }

    // 模型尚未完工，暂时弹窗提示用户
    setPredictionError(null)
    setPredictionData(null)
    setShowModelDialog(true)

    // 保留接口调用逻辑，待模型上线后启用
    // onLoadingChange?.(true)
    // try {
    //   const response = await predictTrend(fileId, predictionDays)
    //   setPredictionData(response)
    // } catch (error: any) {
    //   const errorMessage =
    //     error.response?.data?.detail || error.message || '预测失败'
    //   setPredictionError(errorMessage)
    // } finally {
    //   onLoadingChange?.(false)
    // }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 relative">
      {/* 标题 */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          K线图（日线）{hasData ? `- ${contractCode}` : `- ${contractCode}`}
        </h3>
        {hasData && (
          <p className="text-sm text-gray-500 mt-1">
            已加载 {csvData?.length} 条数据
          </p>
        )}
      </div>

      {/* K线图区域 */}
      {hasData ? (
        <div className="w-full mb-4">
          <CandlestickChart data={csvData || []} showVolume={true} />
        </div>
      ) : (
        <div className="w-full h-96 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center mb-4">
          <div className="text-center">
            <div className="text-4xl mb-4">📈</div>
            <p className="text-gray-500 text-lg">K线图区域（日线）</p>
            <p className="text-gray-400 text-xs mt-1">
              （请上传CSV数据以显示K线图）
            </p>
          </div>
        </div>
      )}

      {/* 预测控制区域 */}
      {hasData && fileId && (
        <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-center gap-4 flex-wrap">
            <label htmlFor="predictionDays" className="text-sm font-medium text-gray-700">
              预测未来天数：
            </label>
            <input
              id="predictionDays"
              type="number"
              min="1"
              max="30"
              value={predictionDays}
              onChange={(e) => setPredictionDays(parseInt(e.target.value) || 1)}
              className="border border-gray-300 rounded-lg px-3 py-1 w-20 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={predicting}
            />
            <button
              onClick={handlePredict}
              disabled={predicting}
              className={`px-6 py-2 rounded-lg font-medium text-white transition-colors ${
                predicting
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {predicting ? '预测中...' : '开始预测'}
            </button>
          </div>

          {/* 预测错误提示 */}
          {predictionError && (
            <div className="mt-3 bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded text-sm">
              {predictionError}
            </div>
          )}
        </div>
      )}

      {/* 预测结果展示 */}
      {predictionData && Array.isArray(predictionData.predictions) && (
        <div className="mt-4 space-y-4">
          <h4 className="text-base font-semibold text-gray-800">预测结果</h4>
          
          {/* 统计卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-600 mb-1">趋势方向</p>
              <p className="text-2xl font-bold text-blue-600">
                {predictionData.trend || '未知'}
              </p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <p className="text-sm text-gray-600 mb-1">置信度</p>
              <p className="text-2xl font-bold text-green-600">
                {predictionData.confidence
                  ? `${(predictionData.confidence * 100).toFixed(1)}%`
                  : 'N/A'}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <p className="text-sm text-gray-600 mb-1">预测天数</p>
              <p className="text-2xl font-bold text-purple-600">
                {predictionData.metadata?.prediction_days || predictionDays}
              </p>
            </div>
          </div>

          {/* 预测图表 */}
          <div className="mt-4">
            <Chart
              predictions={predictionData.predictions}
              trend={predictionData.trend}
            />
          </div>

          {/* 详细预测值 */}
          <div className="mt-4">
            <h5 className="text-sm font-medium text-gray-700 mb-2">详细预测值</h5>
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
        </div>
      )}

      {/* 模型建设中提示弹窗 */}
      {showModelDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-gray-900/50" aria-hidden="true" />
          <div className="relative w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
            <h4 className="text-lg font-semibold text-gray-800 mb-2">模型建设中</h4>
            <p className="text-sm text-gray-600 leading-relaxed">
              预测引擎仍在开发整合中，暂无法提供即时预测结果。
              我们正在加速部署 Kronos 模型，敬请期待后续更新。
            </p>
            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setShowModelDialog(false)}
                className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors"
              >
                知道了
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
