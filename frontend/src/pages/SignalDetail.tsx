import { useParams, useNavigate } from 'react-router-dom'
import MainLayout from '../components/layout/MainLayout'

export default function SignalDetail() {
  const { id } = useParams()
  const navigate = useNavigate()

  // Mock Data (In real app, fetch by id)
  const detail = {
    id,
    title: '沪深300股指期货(IF2312) 关键点位分析与操作建议',
    contractCode: 'IF2312',
    contractName: '沪深300',
    publishTime: '2023-11-24 10:30',
    author: '首席分析师',
    stopLoss: 3520.0,
    takeProfit: 3620.0,
    content: `
      今日沪深300股指期货(IF2312)早盘小幅低开后震荡上行，目前站稳3550一线。
      
      从技术面来看：
      1. 日线级别MACD指标出现底部金叉，红柱开始放出，显示反弹动能增强。
      2. KDJ指标在超卖区域形成金叉向上发散。
      3. 30分钟级别突破下行趋势线压制。
      
      基本面方面：
      近期宏观政策利好频出，市场情绪有所回暖，北向资金出现净流入迹象。
      
      操作建议：
      建议激进投资者在3550-3560区间分批尝试建立多单。
      止损位严格设置在3520下方。
      第一目标位看至3620附近，若突破可进一步上看3650。
      
      风险提示：
      需关注午后成交量配合情况，若成交量无法有效放大，可能面临冲高回落风险。
    `
  }

  return (
    <MainLayout user={{ nickname: 'User', user_role: 2 }} onLogout={() => {}}>
      <div className="grid grid-cols-12 gap-6 max-w-7xl mx-auto h-[calc(100vh-8rem)]">
        {/* Left Column: Content */}
        <div className="col-span-9 bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-full">
           {/* Header */}
           <div className="p-6 border-b border-gray-100">
              <div className="flex items-center gap-3 mb-3">
                 <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded">
                    {detail.contractName}
                 </span>
                 <span className="text-sm text-gray-500">{detail.contractCode}</span>
                 <span className="ml-auto text-sm text-gray-400">{detail.publishTime}</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-4">{detail.title}</h1>
              
              <div className="flex gap-4">
                 <div className="flex items-center gap-2 px-4 py-2 bg-red-50 rounded-lg border border-red-100">
                    <span className="text-xs text-red-500">止损参考</span>
                    <span className="font-mono font-bold text-red-700">{detail.stopLoss}</span>
                 </div>
                 <div className="flex items-center gap-2 px-4 py-2 bg-green-50 rounded-lg border border-green-100">
                    <span className="text-xs text-green-500">止盈参考</span>
                    <span className="font-mono font-bold text-green-700">{detail.takeProfit}</span>
                 </div>
              </div>
           </div>

           {/* Scrollable Content Area */}
           <div className="flex-1 overflow-y-auto p-8">
              {/* Chart Placeholder */}
              <div className="w-full h-64 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 flex items-center justify-center mb-8">
                  <div className="text-center text-gray-400">
                      <svg className="w-12 h-12 mx-auto mb-2 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" /></svg>
                      <span className="text-sm font-medium">K 线分析图表</span>
                  </div>
              </div>

              {/* Text Content */}
              <div className="prose max-w-none text-gray-700 whitespace-pre-line leading-relaxed">
                 {detail.content}
              </div>
           </div>

           {/* Footer Actions */}
           <div className="p-4 border-t border-gray-100 bg-gray-50 flex justify-between items-center">
              <button 
                onClick={() => navigate(-1)}
                className="px-4 py-2 text-gray-500 hover:bg-gray-200 rounded-lg transition-colors text-sm"
              >
                 ← 返回列表
              </button>
              <div className="flex gap-3">
                 <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 text-gray-600 transition-colors">
                    <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
                    <span>收藏</span>
                 </button>
                 <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-sm">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" /></svg>
                    <span>点赞 (128)</span>
                 </button>
              </div>
           </div>
        </div>

        {/* Right Column: Author Info */}
        <div className="col-span-3 flex flex-col gap-6">
           <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
              <div className="w-20 h-20 mx-auto bg-gray-200 rounded-full mb-4 overflow-hidden">
                 {/* Placeholder Avatar */}
                 <svg className="w-full h-full text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
              </div>
              <h3 className="font-bold text-gray-900 text-lg">{detail.author}</h3>
              <p className="text-xs text-gray-500 mt-1">认证分析师 / 资深交易员</p>
              
              <button className="mt-4 w-full py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 font-medium text-sm transition-colors">
                 查看主页
              </button>
           </div>

           <div className="bg-blue-600 rounded-xl shadow-lg p-6 text-white">
              <h4 className="font-bold text-lg mb-2">开通 VIP 会员</h4>
              <p className="text-sm opacity-90 mb-4">解锁更多深度分析和实时交易信号提示。</p>
              <button className="w-full py-2 bg-white text-blue-600 rounded-lg font-bold hover:bg-gray-50 transition-colors text-sm">
                 立即升级
              </button>
           </div>
        </div>
      </div>
    </MainLayout>
  )
}

