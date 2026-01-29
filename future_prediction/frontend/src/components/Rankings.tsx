/** 板块榜单组件。
 *
 * 显示板块排名，点击板块后显示该板块内合约的排名。
 */

import { useState } from 'react'

/** 板块信息接口。 */
interface Sector {
  /** 板块ID。 */
  sectorId: number
  /** 板块代码。 */
  sectorCode: string
  /** 板块名称。 */
  sectorName: string
  /** 板块涨跌幅（%）。 */
  changePercent: number
  /** 板块成交额（万元）。 */
  turnover: number
  /** 板块内合约数量。 */
  contractCount: number
}

/** 合约信息接口。 */
interface Contract {
  /** 合约代码。 */
  contractCode: string
  /** 合约名称。 */
  contractName: string
  /** 涨跌幅（%）。 */
  changePercent: number
  /** 成交额（万元）。 */
  turnover: number
  /** 当前价格。 */
  currentPrice: number
  /** 波动率（%）。 */
  volatility: number
}

/** 板块榜单组件的属性接口。 */
interface RankingsProps {
  /** 是否为会员（决定显示数量）。 */
  isMember?: boolean
}

/**
 * 板块榜单组件。
 * 
 * @param props - 组件属性。
 * @returns JSX 元素。
 */
export default function Rankings({ isMember = false }: RankingsProps) {
  /** 当前选中的板块。 */
  const [selectedSector, setSelectedSector] = useState<Sector | null>(null)
  /** 搜索关键词 */
  const [searchTerm, setSearchTerm] = useState('')

  /** Mock 板块数据。 */
  const mockSectors: Sector[] = [
    { sectorId: 1, sectorCode: 'METAL', sectorName: '金属', changePercent: 2.35, turnover: 125000, contractCount: 15 },
    { sectorId: 2, sectorCode: 'ENERGY', sectorName: '能源', changePercent: 1.85, turnover: 98000, contractCount: 12 },
    { sectorId: 3, sectorCode: 'AGRICULTURE', sectorName: '农产品', changePercent: -0.65, turnover: 75000, contractCount: 18 },
    { sectorId: 4, sectorCode: 'CHEMICAL', sectorName: '化工', changePercent: 0.95, turnover: 65000, contractCount: 10 },
    { sectorId: 5, sectorCode: 'FINANCE', sectorName: '金融', changePercent: 1.25, turnover: 145000, contractCount: 8 },
    { sectorId: 6, sectorCode: 'STOCK_INDEX', sectorName: '股指', changePercent: 0.45, turnover: 185000, contractCount: 5 },
  ]

  /** Mock 合约数据。 */
  const getMockContracts = (sectorCode: string): Contract[] => {
    const baseContracts: Record<string, Contract[]> = {
      'METAL': [
        { contractCode: 'CU2312', contractName: '沪铜2312', changePercent: 2.15, turnover: 25000, currentPrice: 68500, volatility: 1.2 },
        { contractCode: 'AL2312', contractName: '沪铝2312', changePercent: 1.85, turnover: 18000, currentPrice: 18500, volatility: 0.9 },
        { contractCode: 'ZN2312', contractName: '沪锌2312', changePercent: 2.45, turnover: 15000, currentPrice: 21500, volatility: 1.5 },
        { contractCode: 'NI2312', contractName: '沪镍2312', changePercent: 3.25, turnover: 22000, currentPrice: 145000, volatility: 2.1 },
        { contractCode: 'PB2312', contractName: '沪铅2312', changePercent: 1.25, turnover: 8000, currentPrice: 16500, volatility: 0.8 },
      ],
      'ENERGY': [
        { contractCode: 'SC2312', contractName: '原油2312', changePercent: 1.65, turnover: 35000, currentPrice: 520, volatility: 1.8 },
        { contractCode: 'FU2312', contractName: '燃料油2312', changePercent: 2.15, turnover: 18000, currentPrice: 3200, volatility: 1.5 },
        { contractCode: 'LU2312', contractName: '低硫燃料油2312', changePercent: 1.95, turnover: 12000, currentPrice: 4100, volatility: 1.3 },
      ],
      'AGRICULTURE': [
        { contractCode: 'C2312', contractName: '玉米2312', changePercent: -0.45, turnover: 15000, currentPrice: 2650, volatility: 0.6 },
        { contractCode: 'M2312', contractName: '豆粕2312', changePercent: -0.85, turnover: 18000, currentPrice: 3850, volatility: 0.8 },
        { contractCode: 'Y2312', contractName: '豆油2312', changePercent: 0.25, turnover: 12000, currentPrice: 7850, volatility: 1.1 },
      ],
    }
    return baseContracts[sectorCode] || []
  }

  /** 排序后的板块列表。 */
  const sortedSectors = [...mockSectors].sort((a, b) => 
    b.changePercent - a.changePercent
  ).filter(s => s.sectorName.includes(searchTerm) || s.sectorCode.includes(searchTerm.toUpperCase()))

  /** 显示的板块数量。 */
  const displaySectors = isMember ? sortedSectors : sortedSectors.slice(0, 3)

  /** 当前板块的合约列表。 */
  const contracts = selectedSector ? getMockContracts(selectedSector.sectorCode) : []

  /** 排序后的合约列表（按涨跌幅）。 */
  const sortedContracts = [...contracts].sort((a, b) => 
    b.changePercent - a.changePercent
  ).filter(c => c.contractName.includes(searchTerm) || c.contractCode.includes(searchTerm.toUpperCase()))

  /**
   * 处理板块点击。
   * 
   * @param sector - 选中的板块。
   */
  const handleSectorClick = (sector: Sector) => {
    setSelectedSector(sector)
    setSearchTerm('') // 重置搜索
  }

  /**
   * 返回板块列表。
   */
  const handleBack = () => {
    setSelectedSector(null)
    setSearchTerm('')
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-0 overflow-hidden h-full flex flex-col">
      {/* 标题栏 */}
      <div className="p-4 border-b border-gray-100 bg-gray-50/50">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-bold text-gray-800">
            {selectedSector ? selectedSector.sectorName : '板块风云榜'}
          </h3>
          {selectedSector && (
            <button
              onClick={handleBack}
              className="text-xs text-blue-600 hover:text-blue-700 bg-blue-50 px-2 py-1 rounded flex items-center gap-1 hover:bg-blue-100 transition-colors"
            >
              <span>←</span> 返回
            </button>
          )}
        </div>
        
        {/* 搜索框 */}
        <div className="relative">
           <input
             type="text"
             placeholder={selectedSector ? `搜索 ${selectedSector.sectorName} 合约...` : "搜索板块..."}
             value={searchTerm}
             onChange={(e) => setSearchTerm(e.target.value)}
             className="w-full pl-8 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
           />
           <svg className="w-4 h-4 text-gray-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
           </svg>
        </div>
      </div>

      {/* 权限提示 */}
      {!selectedSector && !isMember && (
        <div className="px-4 py-2 bg-amber-50 border-b border-amber-100">
          <p className="text-xs text-amber-700 flex items-center gap-2">
             <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
             </svg>
             普通用户仅展示前 3 名，会员查看全部
          </p>
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
         {!selectedSector ? (
           /* 板块列表（第一级） */
           <table className="w-full">
             <thead className="bg-gray-50 text-xs text-gray-500 sticky top-0 z-10">
               <tr>
                 <th className="text-left py-2 px-4 font-medium">排名</th>
                 <th className="text-left py-2 px-4 font-medium">板块</th>
                 <th className="text-right py-2 px-4 font-medium">涨幅</th>
               </tr>
             </thead>
             <tbody>
               {displaySectors.map((sector, index) => {
                 const isPositive = sector.changePercent >= 0
                 return (
                   <tr
                     key={sector.sectorId}
                     className="border-b border-gray-50 hover:bg-blue-50/50 cursor-pointer transition-colors group"
                     onClick={() => handleSectorClick(sector)}
                   >
                     <td className="py-3 px-4 text-sm text-gray-600 w-16">
                       <span className={`inline-flex items-center justify-center w-6 h-6 rounded text-xs font-bold ${
                         index < 3 ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-500'
                       }`}>
                         {index + 1}
                       </span>
                     </td>
                     <td className="py-3 px-4 text-sm font-medium text-gray-800">
                       <div className="flex flex-col">
                          <span>{sector.sectorName}</span>
                          <span className="text-[10px] text-gray-400 font-normal group-hover:text-blue-400">{sector.sectorCode}</span>
                       </div>
                     </td>
                     <td className={`py-3 px-4 text-sm text-right font-bold ${
                       isPositive ? 'text-red-600' : 'text-green-600'
                     }`}>
                       {isPositive ? '+' : ''}{sector.changePercent.toFixed(2)}%
                     </td>
                   </tr>
                 )
               })}
             </tbody>
           </table>
         ) : (
           /* 板块内合约列表（第二级） */
           <div>
             {/* 头部摘要 */}
             <div className="p-3 bg-blue-50/30 grid grid-cols-3 gap-2 border-b border-blue-100">
                 <div className="text-center">
                    <p className="text-[10px] text-gray-500">涨跌幅</p>
                    <p className={`font-bold text-sm ${selectedSector.changePercent >= 0 ? 'text-red-600' : 'text-green-600'}`}>
                       {selectedSector.changePercent >= 0 ? '+' : ''}{selectedSector.changePercent}%
                    </p>
                 </div>
                 <div className="text-center border-l border-gray-200">
                    <p className="text-[10px] text-gray-500">成交额</p>
                    <p className="font-bold text-gray-800 text-sm">{selectedSector.turnover > 10000 ? (selectedSector.turnover/10000).toFixed(1)+'亿' : selectedSector.turnover+'万'}</p>
                 </div>
                 <div className="text-center border-l border-gray-200">
                    <p className="text-[10px] text-gray-500">合约数</p>
                    <p className="font-bold text-gray-800 text-sm">{selectedSector.contractCount}</p>
                 </div>
             </div>

             <table className="w-full">
               <thead className="bg-gray-50 text-xs text-gray-500 sticky top-0 z-10">
                 <tr>
                   <th className="text-left py-2 px-4 font-medium">合约</th>
                   <th className="text-right py-2 px-4 font-medium">最新价</th>
                   <th className="text-right py-2 px-4 font-medium">涨跌幅</th>
                 </tr>
               </thead>
               <tbody>
                 {sortedContracts.map((contract) => {
                   const isPositive = contract.changePercent >= 0
                   return (
                     <tr
                       key={contract.contractCode}
                       className="border-b border-gray-50 hover:bg-gray-50 transition-colors"
                     >
                       <td className="py-2 px-4 text-sm font-medium text-gray-800">
                         <div className="flex flex-col">
                            <span>{contract.contractName}</span>
                            <span className="text-[10px] text-gray-400 font-normal">{contract.contractCode}</span>
                         </div>
                       </td>
                       <td className="py-2 px-4 text-sm text-right text-gray-800 font-mono">
                         {contract.currentPrice.toLocaleString()}
                       </td>
                       <td className={`py-2 px-4 text-sm text-right font-bold ${
                         isPositive ? 'text-red-600' : 'text-green-600'
                       }`}>
                         {isPositive ? '+' : ''}{contract.changePercent.toFixed(2)}%
                       </td>
                     </tr>
                   )
                 })}
               </tbody>
             </table>

             {sortedContracts.length === 0 && (
               <div className="text-center py-8 text-gray-400">
                 <p>无匹配合约</p>
               </div>
             )}
           </div>
         )}
      </div>

      {/* 底部提示 */}
      <div className="p-2 bg-gray-50 border-t border-gray-100 text-center text-[10px] text-gray-400">
        数据每 5 秒自动刷新
      </div>
    </div>
  )
}
