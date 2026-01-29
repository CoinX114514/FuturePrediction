/** K 线图表组件。

使用 TradingView lightweight-charts 展示期货合约的历史 K 线图。
*/

import { useEffect, useRef } from 'react'
import { createChart, IChartApi, ISeriesApi, CandlestickData, Time, CandlestickSeries } from 'lightweight-charts'
import axios from 'axios'

/** API 基础 URL。 */
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 
  (import.meta.env.MODE === 'development' ? '/api' : 'http://localhost:8000/api')

/** 创建 axios 实例。 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 添加请求拦截器，自动添加 Token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/** K 线数据接口。 */
interface KlineData {
  time: string
  open: number
  high: number
  low: number
  close: number
  volume?: number
}

/** K 线图表组件属性。 */
interface KlineChartProps {
  /** 合约代码，如 "IF2312"。 */
  contractCode: string
  /** 图表高度，默认 400px。 */
  height?: number
  /** 获取最近多少天的数据，默认 365 天。 */
  period?: number
}

/**
 * K 线图表组件。
 * 
 * @param props - 组件属性。
 */
export default function KlineChart({ contractCode, height = 400, period = 365 }: KlineChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null)

  useEffect(() => {
    if (!chartContainerRef.current) return

    // 创建图表实例
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: height,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#e0e0e0' },
        horzLines: { color: '#e0e0e0' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      rightPriceScale: {
        borderColor: '#cccccc',
      },
    })

    chartRef.current = chart

    // 创建 K 线系列
    // 注意：lightweight-charts 5.0+ 使用 addSeries 替代 addCandlestickSeries
    const candlestickSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
    })

    seriesRef.current = candlestickSeries

    // 获取 K 线数据
    const fetchKlineData = async () => {
      try {
        const response = await apiClient.get(`/v1/kline/${contractCode}`, {
          params: { period },
        })

        const klineData: KlineData[] = response.data.data || []

        if (klineData.length === 0) {
          console.warn(`未找到合约 ${contractCode} 的 K 线数据`)
          return
        }

        // 转换数据格式为 lightweight-charts 需要的格式
        const chartData: CandlestickData[] = klineData.map((item) => ({
          time: item.time as Time, // 日期字符串，如 "2024-01-01"
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
        }))

        // 设置数据
        candlestickSeries.setData(chartData)

        // 调整图表以适应数据
        chart.timeScale().fitContent()
      } catch (error: any) {
        console.error('获取 K 线数据失败:', error)
        // 可以在这里显示错误提示
      }
    }

    fetchKlineData()

    /** 与后端现价同步：每 5 分钟刷新 K 线数据（最后一根与现价一致） */
    const PRICE_REFRESH_INTERVAL_MS = 5 * 60 * 1000
    const refreshTimer = setInterval(fetchKlineData, PRICE_REFRESH_INTERVAL_MS)

    // 响应窗口大小变化
    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        })
      }
    }

    window.addEventListener('resize', handleResize)

    // 清理函数
    return () => {
      clearInterval(refreshTimer)
      window.removeEventListener('resize', handleResize)
      if (chartRef.current) {
        chartRef.current.remove()
        chartRef.current = null
      }
    }
  }, [contractCode, height, period])

  return (
    <div className="w-full">
      <div ref={chartContainerRef} style={{ width: '100%', height: `${height}px` }} />
    </div>
  )
}

