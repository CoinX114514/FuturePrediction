import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

/** 圖表組件的屬性接口。 */
interface ChartProps {
  /** 預測值陣列。 */
  predictions?: number[]
  /** 趨勢方向。 */
  trend?: string
}

/** 價格趨勢預測圖表組件。
 * 
 * 使用 Recharts 庫可視化預測結果。
 * 
 * @param props - 組件屬性。
 */
function Chart({ predictions, trend }: ChartProps) {
  /** 安全處理預測數據。 */
  const safePredictions = Array.isArray(predictions) ? predictions : []

  /** 如果暫無數據，顯示提示。 */
  if (safePredictions.length === 0) {
    return (
      <div className="w-full rounded-lg border border-dashed border-gray-300 p-6 text-center text-sm text-gray-500">
        目前尚無可視化的預測數據，待模型完成後將自動顯示。
      </div>
    )
  }

  /** 準備圖表數據。 */
  const chartData = safePredictions.map((value, index) => ({
    day: `第 ${index + 1} 天`,
    value: value * 100, // 轉換為百分比
    dayIndex: index + 1,
  }))

  /** 根據趨勢確定線條顏色。 */
  const getLineColor = () => {
    if (trend === '上涨' || trend === '上漲') {
      return '#10b981' // 綠色
    } else if (trend === '下跌') {
      return '#ef4444' // 紅色
    } else {
      return '#6366f1' // 藍色（震蕩）
    }
  }

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        預測趨勢圖表
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="day"
            tick={{ fontSize: 12 }}
            label={{ value: '預測天數', position: 'insideBottom', offset: -5 }}
          />
          <YAxis
            tick={{ fontSize: 12 }}
            label={{
              value: '預測變化 (%)',
              angle: -90,
              position: 'insideLeft',
            }}
          />
          <Tooltip
            formatter={(value: any) => [`${Number(value).toFixed(2)}%`, '預測變化']}
            labelFormatter={(label) => label}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="value"
            stroke={getLineColor()}
            strokeWidth={2}
            name="預測變化 (%)"
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default Chart

