/** 蜡烛图组件。

使用 lightweight-charts 绘制 OHLCV 数据的蜡烛图（K线图）。
成交量独立显示在K线图下方。
*/

import { useEffect, useRef } from 'react'
import { 
  createChart, 
  IChartApi, 
  ISeriesApi, 
  CandlestickData, 
  Time,
  CandlestickSeries,
  HistogramSeries,
} from 'lightweight-charts'

/** OHLCV 数据项接口。 */
export interface OHLCVData {
  /** 日期。 */
  日期: string
  /** 开盘价。 */
  开盘: number
  /** 最高价。 */
  最高: number
  /** 最低价。 */
  最低: number
  /** 收盘价。 */
  收盘: number
  /** 成交量。 */
  成交量: number
}

/** 蜡烛图组件的属性接口。 */
interface CandlestickChartProps {
  /** OHLCV 数据数组。 */
  data: OHLCVData[]
  /** 是否显示成交量。 */
  showVolume?: boolean
}

/**
 * 格式化时间为雅虎财经格式（Nov 6, 2025）。
 * 
 * @param time - 时间戳（秒）。
 * @returns 格式化后的时间字符串。
 */
function formatTimeYahooStyle(time: Time): string {
  const date = new Date((time as number) * 1000)
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const month = monthNames[date.getMonth()]
  const day = date.getDate()
  const year = date.getFullYear()
  
  return `${month} ${day}, ${year}`
}

/**
 * 蜡烛图组件。
 * 
 * @param props - 组件属性。
 * @returns JSX 元素。
 */
export default function CandlestickChart({ 
  data,
  showVolume = true 
}: CandlestickChartProps) {
  /** K线图容器引用。 */
  const klineContainerRef = useRef<HTMLDivElement>(null)
  /** 成交量图容器引用。 */
  const volumeContainerRef = useRef<HTMLDivElement>(null)
  /** Tooltip 容器引用。 */
  const tooltipRef = useRef<HTMLDivElement>(null)
  /** K线图实例引用。 */
  const klineChartRef = useRef<IChartApi | null>(null)
  /** 成交量图实例引用。 */
  const volumeChartRef = useRef<IChartApi | null>(null)
  /** 蜡烛图系列引用。 */
  const candlestickSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null)
  /** 成交量系列引用。 */
  const volumeSeriesRef = useRef<ISeriesApi<'Histogram'> | null>(null)

  // 创建K线图
  useEffect(() => {
    if (!klineContainerRef.current) return

    // 创建K线图
    const chart = createChart(klineContainerRef.current, {
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      width: klineContainerRef.current.clientWidth,
      height: showVolume ? 350 : 400, // 如果显示成交量，K线图高度减少
      grid: {
        vertLines: { color: '#e5e7eb' },
        horzLines: { color: '#e5e7eb' },
      },
      crosshair: {
        mode: 1, // 正常模式
      },
      rightPriceScale: {
        borderColor: '#e5e7eb',
      },
      timeScale: {
        borderColor: '#e5e7eb',
        timeVisible: true,
        secondsVisible: false,
        // 如果显示成交量，隐藏底部时间轴（由成交量图显示）
        visible: !showVolume,
      },
      localization: {
        locale: 'en-US',
        dateFormat: 'MMM d, yyyy', // 雅虎财经格式：Nov 6, 2025
        timeFormatter: formatTimeYahooStyle, // 自定义时间格式化函数
      },
    })

    klineChartRef.current = chart

    // 创建蜡烛图系列
    const candlestickSeriesInstance = chart.addSeries(CandlestickSeries, {
      upColor: '#ef4444', // 涨红（中国习惯）
      downColor: '#10b981', // 跌绿（中国习惯）
      borderVisible: false,
      wickUpColor: '#ef4444',
      wickDownColor: '#10b981',
    })
    candlestickSeriesRef.current = candlestickSeriesInstance as any

    // 订阅十字光标移动事件，显示自定义 tooltip
    chart.subscribeCrosshairMove((param) => {
      if (!tooltipRef.current) return

      if (!param.point || !param.seriesData || param.seriesData.size === 0) {
        // 隐藏 tooltip
        tooltipRef.current.style.display = 'none'
        return
      }

      // 获取当前数据点
      const candlestickData = param.seriesData.get(candlestickSeriesInstance)
      if (!candlestickData || typeof candlestickData === 'string') {
        tooltipRef.current.style.display = 'none'
        return
      }

      // 获取当前数据在数组中的索引
      // 注意：图表中的数据是取前100条、反转、然后按时间戳排序（从早到晚）
      const currentTime = param.time as number
      
      // 取前100条数据，反转，然后按时间戳排序（与图表数据一致）
      const recentData = data
        .slice(0, 100)
        .map((item) => {
          const date = new Date(item.日期)
          const time = Math.floor(date.getTime() / 1000)
          return { ...item, time }
        })
        .reverse()
        .sort((a, b) => a.time - b.time)
      
      // 在数据中查找当前时间对应的索引
      const chartDataIndex = recentData.findIndex((item) => {
        return item.time === currentTime
      })

      if (chartDataIndex === -1) {
        tooltipRef.current.style.display = 'none'
        return
      }

      // 获取当前项和前一项（前一项是时间更早的）
      const currentItem = recentData[chartDataIndex]
      const prevItem = chartDataIndex > 0 ? recentData[chartDataIndex - 1] : null

      // 计算涨跌幅（相对于前一个交易日）
      const { open, high, low, close } = candlestickData as any
      const dayChange = close - open // 当日涨跌
      const dayChangePercent = ((dayChange / open) * 100).toFixed(2)
      
      let prevDayChange = 0
      let prevDayChangePercent = '0.00'
      if (prevItem) {
        prevDayChange = close - prevItem.收盘 // 相对前一日涨跌
        prevDayChangePercent = ((prevDayChange / prevItem.收盘) * 100).toFixed(2)
      }

      // 格式化日期
      const dateStr = formatTimeYahooStyle(currentTime as Time)

      // 构建 tooltip 内容
      const tooltipContent = `
        <div style="font-weight: 600; margin-bottom: 8px; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">
          ${dateStr}
        </div>
        <div style="display: grid; grid-template-columns: 80px 1fr; gap: 4px 12px; font-size: 12px;">
          <div style="color: #6b7280;">开盘:</div>
          <div style="font-weight: 500;">${open.toFixed(2)}</div>
          <div style="color: #6b7280;">最高:</div>
          <div style="color: #ef4444; font-weight: 500;">${high.toFixed(2)}</div>
          <div style="color: #6b7280;">最低:</div>
          <div style="color: #10b981; font-weight: 500;">${low.toFixed(2)}</div>
          <div style="color: #6b7280;">收盘:</div>
          <div style="font-weight: 600; color: ${close >= open ? '#ef4444' : '#10b981'};">
            ${close.toFixed(2)}
          </div>
          <div style="color: #6b7280;">当日涨跌:</div>
          <div style="font-weight: 600; color: ${dayChange >= 0 ? '#ef4444' : '#10b981'};">
            ${dayChange >= 0 ? '+' : ''}${dayChange.toFixed(2)} (${dayChangePercent}%)
          </div>
          ${prevItem ? `
            <div style="color: #6b7280;">相对前日:</div>
            <div style="font-weight: 600; color: ${prevDayChange >= 0 ? '#ef4444' : '#10b981'};">
              ${prevDayChange >= 0 ? '+' : ''}${prevDayChange.toFixed(2)} (${prevDayChangePercent}%)
            </div>
          ` : ''}
          <div style="color: #6b7280;">成交量:</div>
          <div style="font-weight: 500;">${currentItem.成交量.toLocaleString()}</div>
        </div>
      `

      tooltipRef.current.innerHTML = tooltipContent
      tooltipRef.current.style.display = 'block'
      
      // 定位 tooltip（在鼠标右侧显示）
      const chartRect = klineContainerRef.current?.getBoundingClientRect()
      if (chartRect && param.point) {
        const tooltipWidth = 200
        const tooltipHeight = tooltipRef.current.offsetHeight
        let left = param.point.x + 10
        let top = param.point.y - tooltipHeight / 2

        // 确保 tooltip 不超出图表边界
        if (left + tooltipWidth > chartRect.width) {
          left = param.point.x - tooltipWidth - 10
        }
        if (top < 0) {
          top = 10
        }
        if (top + tooltipHeight > chartRect.height) {
          top = chartRect.height - tooltipHeight - 10
        }

        tooltipRef.current.style.left = `${left}px`
        tooltipRef.current.style.top = `${top}px`
      }
    })

    // 处理窗口大小变化
    const handleResize = () => {
      if (klineContainerRef.current && klineChartRef.current) {
        klineChartRef.current.applyOptions({
          width: klineContainerRef.current.clientWidth,
        })
      }
      if (volumeContainerRef.current && volumeChartRef.current) {
        volumeChartRef.current.applyOptions({
          width: volumeContainerRef.current.clientWidth,
        })
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      if (klineChartRef.current) {
        klineChartRef.current.remove()
      }
    }
  }, [showVolume])

  // 创建成交量图
  useEffect(() => {
    if (!showVolume || !volumeContainerRef.current) return

    // 创建成交量图
    const chart = createChart(volumeContainerRef.current, {
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      width: volumeContainerRef.current.clientWidth,
      height: 150, // 成交量图固定高度
      grid: {
        vertLines: { color: '#e5e7eb' },
        horzLines: { color: '#e5e7eb' },
      },
      crosshair: {
        mode: 1, // 正常模式
      },
      rightPriceScale: {
        borderColor: '#e5e7eb',
        visible: true,
      },
      leftPriceScale: {
        visible: false, // 隐藏左侧价格刻度
      },
      timeScale: {
        borderColor: '#e5e7eb',
        timeVisible: true,
        secondsVisible: false,
      },
      localization: {
        locale: 'en-US',
        dateFormat: 'MMM d, yyyy', // 雅虎财经格式：Nov 6, 2025
        timeFormatter: formatTimeYahooStyle, // 自定义时间格式化函数
      },
    })

    volumeChartRef.current = chart

    // 创建成交量系列
    const volumeSeriesInstance = chart.addSeries(HistogramSeries, {
      priceFormat: {
        type: 'volume',
      },
    })
    volumeSeriesRef.current = volumeSeriesInstance as any

    // 注意：时间轴同步将在数据设置完成后进行

    return () => {
      if (volumeChartRef.current) {
        volumeChartRef.current.remove()
      }
    }
  }, [showVolume])

  // 更新数据
  useEffect(() => {
    if (!data || data.length === 0) return
    if (!candlestickSeriesRef.current) return

    // 保持CSV的原始顺序，不排序
    // CSV是从新到旧排列（第一行是最新的，最后一行是最旧的）
    // 取前100条数据（最新的100条）
    const recentData = data.slice(0, 100)

    // 转换数据格式
    // lightweight-charts要求数据按时间升序排列（从早到晚）
    // 由于CSV是从新到旧，需要反转数组，然后按时间戳排序确保升序
    const candlestickData: CandlestickData[] = recentData
      .map((item) => {
        // 将日期字符串转换为时间戳（秒）
        // 日期格式可能是 "Nov 6, 2025" 或 "2025-11-06"
        const date = new Date(item.日期)
        const time = (date.getTime() / 1000) as Time

        return {
          time,
          open: item.开盘,
          high: item.最高,
          low: item.最低,
          close: item.收盘,
        }
      })
      .reverse() // 反转：从新到旧 -> 从早到晚
      .sort((a, b) => (a.time as number) - (b.time as number)) // 按时间戳升序排序，确保数据正确排序

    // 设置蜡烛图数据
    candlestickSeriesRef.current.setData(candlestickData)

    // 如果显示成交量，设置成交量数据
    if (showVolume && volumeSeriesRef.current) {
      // 使用与K线图相同的数据处理逻辑：保持原始顺序，取前100条（最新的）
      const recentData = data.slice(0, 100)

      const volumeData = recentData
        .map((item) => {
          const date = new Date(item.日期)
          const time = (date.getTime() / 1000) as Time
          const isUp = item.收盘 >= item.开盘

          return {
            time,
            value: item.成交量,
            // 涨红跌绿，透明度30%
            color: isUp 
              ? 'rgba(239, 68, 68, 0.3)' // 涨红，30%不透明度
              : 'rgba(16, 185, 129, 0.3)', // 跌绿，30%不透明度
          }
        })
        .reverse() // 反转：从新到旧 -> 从早到晚
        .sort((a, b) => (a.time as number) - (b.time as number)) // 按时间戳升序排序，确保数据正确排序

      volumeSeriesRef.current.setData(volumeData)
    }

    // 自动缩放以适应数据
    if (klineChartRef.current) {
      klineChartRef.current.timeScale().fitContent()
    }
    if (showVolume && volumeChartRef.current) {
      volumeChartRef.current.timeScale().fitContent()
    }

    // 在数据设置完成后，同步时间轴和十字光标
    if (showVolume && klineChartRef.current && volumeChartRef.current) {
      const klineTimeScale = klineChartRef.current.timeScale()
      const volumeTimeScale = volumeChartRef.current.timeScale()

      // 同步时间轴范围（延迟执行，确保数据已加载）
      setTimeout(() => {
        try {
          const klineRange = klineTimeScale.getVisibleRange()
          if (klineRange && klineRange.from && klineRange.to) {
            volumeTimeScale.setVisibleRange(klineRange)
          }
        } catch (error) {
          // 忽略错误，数据可能还未完全加载
        }
      }, 100)

      // 监听K线图的时间轴变化，同步到成交量图
      klineTimeScale.subscribeVisibleTimeRangeChange((timeRange) => {
        if (timeRange && timeRange.from && timeRange.to && volumeChartRef.current) {
          try {
            volumeTimeScale.setVisibleRange(timeRange)
          } catch (error) {
            // 忽略错误
          }
        }
      })

      // 监听成交量图的时间轴变化，同步到K线图
      volumeTimeScale.subscribeVisibleTimeRangeChange((timeRange) => {
        if (timeRange && timeRange.from && timeRange.to && klineChartRef.current) {
          try {
            klineTimeScale.setVisibleRange(timeRange)
          } catch (error) {
            // 忽略错误
          }
        }
      })

      // 注意：十字光标会通过时间轴同步自动同步，无需额外处理
    }
  }, [data, showVolume])

  if (!data || data.length === 0) {
    return (
      <div className="w-full h-96 bg-gray-50 rounded-lg border border-gray-300 flex items-center justify-center">
        <p className="text-gray-500">暂无数据</p>
      </div>
    )
  }

  return (
    <div className="w-full flex flex-col relative">
      {/* K线图 */}
      <div 
        ref={klineContainerRef} 
        className="w-full border-b border-gray-200 relative" 
        style={{ height: showVolume ? '350px' : '400px' }} 
      >
        {/* 自定义 Tooltip */}
        <div
          ref={tooltipRef}
          style={{
            position: 'absolute',
            display: 'none',
            backgroundColor: 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '6px',
            padding: '12px',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            zIndex: 1000,
            pointerEvents: 'none',
            minWidth: '200px',
            fontSize: '12px',
            lineHeight: '1.5',
          }}
        />
      </div>
      
      {/* 成交量图（独立显示） */}
      {showVolume && (
        <div 
          ref={volumeContainerRef} 
          className="w-full" 
          style={{ height: '150px' }} 
        />
      )}
    </div>
  )
}
