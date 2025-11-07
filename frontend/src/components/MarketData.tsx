/** 实时行情模块组件。

显示合约的实时行情数据，包括深度图、成交明细等。
*/

/** 实时行情组件的属性接口。 */
interface MarketDataProps {
  /** 合约代码。 */
  contractCode?: string
}

/**
 * 实时行情模块组件。
 * 
 * @param props - 组件属性。
 * @returns JSX 元素。
 */
export default function MarketData({ contractCode = 'IF2312' }: MarketDataProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        实时行情 - {contractCode}
      </h3>

      {/* 价格信息卡片 */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">最新价</p>
          <p className="text-2xl font-bold text-blue-600">3,245.50</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">涨跌</p>
          <p className="text-2xl font-bold text-green-600">+12.30</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">涨跌幅</p>
          <p className="text-2xl font-bold text-red-600">+0.38%</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">成交量</p>
          <p className="text-2xl font-bold text-purple-600">1,234</p>
        </div>
      </div>

      {/* 深度图占位符 */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-2">深度图</h4>
        <div className="w-full h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl mb-2">📊</div>
            <p className="text-gray-500">深度图区域</p>
            <p className="text-gray-400 text-xs mt-1">（等待后端 API 接入）</p>
          </div>
        </div>
      </div>

      {/* 成交明细占位符 */}
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">成交明细</h4>
        <div className="w-full h-48 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl mb-2">📋</div>
            <p className="text-gray-500">成交明细区域</p>
            <p className="text-gray-400 text-xs mt-1">（等待后端 API 接入）</p>
          </div>
        </div>
      </div>
    </div>
  )
}

