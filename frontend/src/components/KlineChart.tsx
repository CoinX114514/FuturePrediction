/** K 线图表组件。

使用 TradingView lightweight-charts 展示期货合约的历史 K 线图。
*/

import { useEffect, useRef, useState } from 'react'
import {
  createChart,
  IChartApi,
  ISeriesApi,
  CandlestickData,
  Time,
  CandlestickSeries,
} from 'lightweight-charts'
import axios from 'axios'

import { API_BASE_URL } from '../constants/apiBaseUrl'

/** 创建 axios 实例。 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  /** K 线数据量可能较大，与 Nginx proxy_read 对齐 */
  timeout: 120000,
})

/**
 * lightweight-charts v5 日线建议使用 BusinessDay 对象，避免部分环境下字符串 time 不渲染。
 */
function toChartTime(timeStr: string): Time {
  const parts = timeStr.trim().split('-').map((x) => parseInt(x, 10))
  if (parts.length === 3 && parts.every((n) => Number.isFinite(n))) {
    return { year: parts[0], month: parts[1], day: parts[2] } as Time
  }
  return timeStr as Time
}

function resolveChartWidth(el: HTMLDivElement | null): number {
  if (!el) return 320
  const w = el.clientWidth || el.getBoundingClientRect().width
  return Math.max(Math.floor(w), 320)
}

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
  /** 加载或渲染失败时的说明，避免空白无提示 */
  const [chartError, setChartError] = useState<string | null>(null)

  useEffect(() => {
    if (!chartContainerRef.current) return
    setChartError(null)

    // 创建图表实例
    const chart = createChart(chartContainerRef.current, {
      width: resolveChartWidth(chartContainerRef.current),
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
        const response = await apiClient.get(`/v1/kline/${encodeURIComponent(contractCode)}`, {
          params: { period },
        })

        const klineData: KlineData[] = response.data?.data || []

        if (klineData.length === 0) {
          const msg = `未找到合约 ${contractCode} 的 K 线数据（后端返回空数组）`
          console.warn(msg)
          setChartError(msg)
          return
        }

        const chartData: CandlestickData[] = klineData.map((item) => ({
          time: toChartTime(item.time),
          open: item.open,
          high: item.high,
          low: item.low,
          close: item.close,
        }))

        try {
          candlestickSeries.setData(chartData)
        } catch (e) {
          console.error('lightweight-charts setData 失败（常见原因：重复 time 或 OHLC 无效）:', e)
          setChartError(`K 线数据格式错误，无法绘图: ${e instanceof Error ? e.message : String(e)}`)
          return
        }

        requestAnimationFrame(() => {
          const el = chartContainerRef.current
          if (el && chartRef.current) {
            chartRef.current.applyOptions({ width: resolveChartWidth(el) })
            chartRef.current.timeScale().fitContent()
          }
        })
        setChartError(null)
      } catch (error: any) {
        const detail = error?.response?.data?.detail
        let msg =
          typeof detail === 'string'
            ? detail
            : Array.isArray(detail)
              ? detail.map((d: { msg?: string }) => d?.msg).filter(Boolean).join('; ')
              : error?.message || ''
        if (!msg) {
          msg = '请求 K 线接口失败（请检查网络、后端是否配置 Tushare 或 JSON klines）'
        }
        console.error('获取 K 线数据失败:', error)
        setChartError(msg)
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
    <div className="w-full space-y-2">
      {chartError && (
        <div className="rounded border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
          K 线图：{chartError}
        </div>
      )}
      <div ref={chartContainerRef} style={{ width: '100%', minWidth: '320px', height: `${height}px` }} />
    </div>
  )
}

