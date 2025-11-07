/** 基础信息栏组件。

显示合约详情、持仓分析、资金流向。
*/

/** 基础信息栏组件的属性接口。 */
interface ContractInfoProps {
  /** 合约代码。 */
  contractCode?: string
}

/**
 * 基础信息栏组件。
 * 
 * @param props - 组件属性。
 * @returns JSX 元素。
 */
export default function ContractInfo({ contractCode = 'IF2312' }: ContractInfoProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">基础信息</h3>

      {/* 合约详情 */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3">合约详情</h4>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-xs text-gray-500 mb-1">合约代码</p>
            <p className="text-sm font-medium text-gray-800">{contractCode}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">交易所</p>
            <p className="text-sm font-medium text-gray-800">CFFEX</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">合约乘数</p>
            <p className="text-sm font-medium text-gray-800">300</p>
          </div>
          <div>
            <p className="text-xs text-gray-500 mb-1">最小变动价位</p>
            <p className="text-sm font-medium text-gray-800">0.2</p>
          </div>
        </div>
      </div>

      {/* 持仓分析占位符 */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-2">持仓分析</h4>
        <div className="w-full h-32 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-2xl mb-1">📊</div>
            <p className="text-gray-500 text-sm">持仓分析图表</p>
            <p className="text-gray-400 text-xs mt-1">（等待后端 API 接入）</p>
          </div>
        </div>
      </div>

      {/* 资金流向占位符 */}
      <div>
        <h4 className="text-sm font-medium text-gray-700 mb-2">资金流向</h4>
        <div className="w-full h-32 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center">
          <div className="text-center">
            <div className="text-2xl mb-1">💰</div>
            <p className="text-gray-500 text-sm">资金流向图表</p>
            <p className="text-gray-400 text-xs mt-1">（等待后端 API 接入）</p>
          </div>
        </div>
      </div>
    </div>
  )
}

