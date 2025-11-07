/** AI预测面板组件。

显示预测K线叠加、准确率历史回测、信号强度指示器。
*/

/** AI预测面板组件的属性接口。 */
interface PredictionPanelProps {
  /** 是否有预测数据。 */
  hasPrediction?: boolean
  /** 预测数据。 */
  predictionData?: any
}

/**
 * AI预测面板组件。
 * 
 * @param props - 组件属性。
 * @returns JSX 元素。
 */
export default function PredictionPanel({ 
  hasPrediction = false,
  predictionData 
}: PredictionPanelProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">AI预测面板</h3>

      {/* 预测K线叠加显示 */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-2">预测K线叠加</h4>
        <div className="w-full h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl mb-2">🔮</div>
            <p className="text-gray-500">
              {hasPrediction ? '预测K线叠加显示' : '暂无预测数据'}
            </p>
            <p className="text-gray-400 text-xs mt-1">
              {hasPrediction ? '（等待后端 API 接入）' : '请先上传数据并执行预测'}
            </p>
          </div>
        </div>
      </div>

      {/* 准确率历史回测 */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-2">准确率历史回测</h4>
        <div className="w-full h-48 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl mb-2">📈</div>
            <p className="text-gray-500">准确率回测图表</p>
            <p className="text-gray-400 text-xs mt-1">（等待后端 API 接入）</p>
          </div>
        </div>
      </div>

      {/* 信号强度指示器 */}
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">信号强度</h4>
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">买入信号</span>
              <span className="text-sm font-medium text-green-600">75%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all"
                style={{ width: '75%' }}
              ></div>
            </div>
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">卖出信号</span>
              <span className="text-sm font-medium text-red-600">25%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-red-500 h-2 rounded-full transition-all"
                style={{ width: '25%' }}
              ></div>
            </div>
          </div>
        </div>
        <p className="text-xs text-gray-400 mt-2 text-center">
          （等待后端 API 接入真实数据）
        </p>
      </div>
    </div>
  )
}

