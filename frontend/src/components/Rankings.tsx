/** 板块榜单组件。

显示板块排名，点击板块后显示该板块内合约的排名。
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
  )

  /** 显示的板块数量。 */
  const displaySectors = isMember ? sortedSectors : sortedSectors.slice(0, 3)

  /** 当前板块的合约列表。 */
  const contracts = selectedSector ? getMockContracts(selectedSector.sectorCode) : []

  /** 排序后的合约列表（按涨跌幅）。 */
  const sortedContracts = [...contracts].sort((a, b) => 
    b.changePercent - a.changePercent
  )

  /**
   * 处理板块点击。
   * 
   * @param sector - 选中的板块。
   */
  const handleSectorClick = (sector: Sector) => {
    setSelectedSector(sector)
  }

  /**
   * 返回板块列表。
   */
  const handleBack = () => {
    setSelectedSector(null)
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* 标题 */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">板块榜单</h3>
        {selectedSector && (
          <button
            onClick={handleBack}
            className="text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            <span>←</span> 返回板块列表
          </button>
        )}
      </div>

      {/* 权限提示 */}
      {!selectedSector && !isMember && (
        <div className="mb-4 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-2 rounded-lg text-sm">
          <p>普通用户仅可查看前 3 个板块，升级会员查看全部板块</p>
        </div>
      )}

      {!selectedSector ? (
        /* 板块列表（第一级） */
        <div className="space-y-2">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 px-4 text-sm font-medium text-gray-700">排名</th>
                  <th className="text-left py-2 px-4 text-sm font-medium text-gray-700">板块名称</th>
                  <th className="text-right py-2 px-4 text-sm font-medium text-gray-700">涨跌幅</th>
                  <th className="text-right py-2 px-4 text-sm font-medium text-gray-700">成交额(万)</th>
                  <th className="text-right py-2 px-4 text-sm font-medium text-gray-700">合约数</th>
                </tr>
              </thead>
              <tbody>
                {displaySectors.map((sector, index) => {
                  const isPositive = sector.changePercent >= 0
                  return (
                    <tr
                      key={sector.sectorId}
                      className="border-b border-gray-100 hover:bg-blue-50 cursor-pointer transition-colors"
                      onClick={() => handleSectorClick(sector)}
                    >
                      <td className="py-3 px-4 text-sm text-gray-600">
                        <span className={`inline-flex items-center justify-center w-6 h-6 rounded ${
                          index < 3 ? 'bg-red-100 text-red-600 font-bold' : 'bg-gray-100 text-gray-600'
                        }`}>
                          {index + 1}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-sm font-medium text-gray-800">
                        {sector.sectorName}
                        <span className="ml-2 text-xs text-gray-500">({sector.sectorCode})</span>
                      </td>
                      <td className={`py-3 px-4 text-sm text-right font-medium ${
                        isPositive ? 'text-red-600' : 'text-green-600'
                      }`}>
                        {isPositive ? '+' : ''}{sector.changePercent.toFixed(2)}%
                      </td>
                      <td className="py-3 px-4 text-sm text-right text-gray-800">
                        {sector.turnover.toLocaleString()}
                      </td>
                      <td className="py-3 px-4 text-sm text-right text-gray-600">
                        {sector.contractCount}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* 板块内合约列表（第二级） */
        <div>
          {/* 板块信息卡片 */}
          <div className="mb-4 bg-blue-50 rounded-lg p-4">
            <h4 className="text-base font-semibold text-gray-800 mb-2">
              {selectedSector.sectorName} ({selectedSector.sectorCode})
            </h4>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <p className="text-gray-600">板块涨跌幅</p>
                <p className={`text-lg font-bold ${
                  selectedSector.changePercent >= 0 ? 'text-red-600' : 'text-green-600'
                }`}>
                  {selectedSector.changePercent >= 0 ? '+' : ''}
                  {selectedSector.changePercent.toFixed(2)}%
                </p>
              </div>
              <div>
                <p className="text-gray-600">板块成交额</p>
                <p className="text-lg font-bold text-gray-800">
                  {selectedSector.turnover.toLocaleString()} 万
                </p>
              </div>
              <div>
                <p className="text-gray-600">合约数量</p>
                <p className="text-lg font-bold text-gray-800">
                  {selectedSector.contractCount}
                </p>
              </div>
            </div>
          </div>

          {/* 合约排名表格 */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 px-4 text-sm font-medium text-gray-700">排名</th>
                  <th className="text-left py-2 px-4 text-sm font-medium text-gray-700">合约代码</th>
                  <th className="text-left py-2 px-4 text-sm font-medium text-gray-700">合约名称</th>
                  <th className="text-right py-2 px-4 text-sm font-medium text-gray-700">当前价</th>
                  <th className="text-right py-2 px-4 text-sm font-medium text-gray-700">涨跌幅</th>
                  <th className="text-right py-2 px-4 text-sm font-medium text-gray-700">成交额(万)</th>
                </tr>
              </thead>
              <tbody>
                {sortedContracts.map((contract, index) => {
                  const isPositive = contract.changePercent >= 0
                  return (
                    <tr
                      key={contract.contractCode}
                      className="border-b border-gray-100 hover:bg-gray-50"
                    >
                      <td className="py-2 px-4 text-sm text-gray-600">
                        <span className={`inline-flex items-center justify-center w-6 h-6 rounded ${
                          index < 3 ? 'bg-red-100 text-red-600 font-bold' : 'bg-gray-100 text-gray-600'
                        }`}>
                          {index + 1}
                        </span>
                      </td>
                      <td className="py-2 px-4 text-sm font-medium text-gray-800">
                        {contract.contractCode}
                      </td>
                      <td className="py-2 px-4 text-sm text-gray-600">{contract.contractName}</td>
                      <td className="py-2 px-4 text-sm text-right text-gray-800">
                        {contract.currentPrice.toLocaleString()}
                      </td>
                      <td className={`py-2 px-4 text-sm text-right font-medium ${
                        isPositive ? 'text-red-600' : 'text-green-600'
                      }`}>
                        {isPositive ? '+' : ''}{contract.changePercent.toFixed(2)}%
                      </td>
                      <td className="py-2 px-4 text-sm text-right text-gray-800">
                        {contract.turnover.toLocaleString()}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {sortedContracts.length === 0 && (
            <div className="text-center py-8 text-gray-400">
              <p>该板块暂无合约数据</p>
            </div>
          )}
        </div>
      )}

      {/* 底部提示 */}
      <div className="mt-4 text-center text-xs text-gray-400">
        <p>数据每 5 秒自动刷新（等待后端 API 接入）</p>
      </div>
    </div>
  )
}
