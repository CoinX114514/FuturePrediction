import React from 'react'

interface SignalCardProps {
  id: number
  title: string
  contractName: string
  contractCode: string
  strikePrice?: number // 行权价 (可选，期货可能没有)
  stopLoss: number
  currentPrice: number
  advice: string
  time: string
  type: 'buy' | 'sell'
}

export default function SignalCard({ 
  title, 
  contractName, 
  contractCode, 
  strikePrice, 
  stopLoss, 
  currentPrice, 
  advice,
  time,
  type
}: SignalCardProps) {
  const isBuy = type === 'buy'
  
  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow p-5 mb-4">
      {/* 头部：标题与时间 */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
            {title}
            <span className={`text-xs px-2 py-0.5 rounded-full border ${
              isBuy ? 'bg-red-50 text-red-600 border-red-200' : 'bg-green-50 text-green-600 border-green-200'
            }`}>
              {isBuy ? '做多' : '做空'}
            </span>
          </h3>
          <p className="text-xs text-gray-400 mt-1">{time}</p>
        </div>
      </div>

      {/* 主要信息网格 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">目标合约</p>
          <p className="font-semibold text-gray-800">{contractName} <span className="text-xs text-gray-400">({contractCode})</span></p>
        </div>
        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">现价</p>
          <p className="font-mono font-semibold text-blue-600">{currentPrice.toLocaleString()}</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">止损价</p>
          <p className="font-mono font-semibold text-gray-700">{stopLoss.toLocaleString()}</p>
        </div>
        {strikePrice && (
          <div className="bg-gray-50 p-3 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">行权价</p>
            <p className="font-mono font-semibold text-gray-700">{strikePrice.toLocaleString()}</p>
          </div>
        )}
      </div>

      {/* 建议内容 */}
      <div className="bg-blue-50/50 border border-blue-100 rounded-lg p-3">
        <p className="text-sm text-gray-700 leading-relaxed">
          <span className="font-bold text-blue-700">建议：</span>
          {advice}
        </p>
      </div>
    </div>
  )
}

