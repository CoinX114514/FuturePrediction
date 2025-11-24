import { useState } from 'react'
import MainLayout from '../components/layout/MainLayout'

export default function AdminPublish() {
  const [title, setTitle] = useState('')
  const [contractCode, setContractCode] = useState('')
  const [stopLoss, setStopLoss] = useState('')
  const [takeProfit, setTakeProfit] = useState('')
  const [content, setContent] = useState('')

  return (
    <MainLayout user={{ nickname: 'Admin', user_role: 3 }} onLogout={() => {}}>
      <div className="grid grid-cols-12 gap-6 h-[calc(100vh-8rem)]">
        {/* Left Column: Inputs & Editor */}
        <div className="col-span-9 flex flex-col gap-4 h-full overflow-y-auto pr-2">
          {/* Header Info */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 space-y-4">
            <div className="flex gap-4">
               <div className="flex-1">
                 <label className="block text-sm font-medium text-gray-700 mb-1">信息标题</label>
                 <input 
                   type="text" 
                   value={title}
                   onChange={(e) => setTitle(e.target.value)}
                   className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                   placeholder="请输入标题..."
                 />
               </div>
            </div>
            
            <div className="grid grid-cols-3 gap-4">
               <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">目标合约代码</label>
                 <div className="relative">
                    <input 
                      type="text" 
                      value={contractCode}
                      onChange={(e) => setContractCode(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                      placeholder="搜索合约 (e.g. IF2312)"
                    />
                    <button className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-600">
                       <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </button>
                 </div>
               </div>
               <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">止损价</label>
                 <input 
                   type="number" 
                   value={stopLoss}
                   onChange={(e) => setStopLoss(e.target.value)}
                   className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                   placeholder="0.00"
                 />
               </div>
               <div>
                 <label className="block text-sm font-medium text-gray-700 mb-1">止盈价 (可选)</label>
                 <input 
                   type="number" 
                   value={takeProfit}
                   onChange={(e) => setTakeProfit(e.target.value)}
                   className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                   placeholder="0.00"
                 />
               </div>
            </div>
          </div>

          {/* Content Editor & Chart Placeholder */}
          <div className="flex-1 flex gap-4 min-h-[500px]">
             {/* Text Editor */}
             <div className="w-1/2 bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col">
                <label className="text-sm font-medium text-gray-700 mb-2">内容正文录入</label>
                <textarea 
                   value={content}
                   onChange={(e) => setContent(e.target.value)}
                   className="flex-1 w-full p-4 bg-gray-50 border border-gray-200 rounded-lg resize-none focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                   placeholder="在此输入详细分析和建议..."
                />
             </div>

             {/* Chart Placeholder */}
             <div className="w-1/2 bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex flex-col">
                <label className="text-sm font-medium text-gray-700 mb-2">合约 K 线图展示 (如有)</label>
                <div className="flex-1 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                   <div className="text-center text-gray-400">
                      <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
                      <p>K 线图表区域</p>
                      <p className="text-xs mt-1">输入合约代码后自动加载</p>
                   </div>
                </div>
             </div>
          </div>
        </div>

        {/* Right Column: Actions & Drafts */}
        <div className="col-span-3 flex flex-col gap-4">
           {/* Action Buttons */}
           <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 space-y-3">
              <button className="w-full py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition-colors shadow-sm">
                 发布
              </button>
              <button className="w-full py-2.5 bg-white border border-blue-200 text-blue-600 rounded-lg hover:bg-blue-50 font-medium transition-colors">
                 保存草稿
              </button>
              <div className="h-px bg-gray-100 my-2"></div>
              <button className="w-full py-2.5 text-red-500 hover:bg-red-50 rounded-lg text-sm transition-colors">
                 删除草稿
              </button>
           </div>

           {/* Draft Box */}
           <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200 flex-1 flex flex-col">
              <h3 className="font-bold text-gray-800 mb-4 flex items-center gap-2">
                 <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                 草稿箱
              </h3>
              <div className="flex-1 overflow-y-auto space-y-2">
                 {[1, 2, 3].map(i => (
                   <div key={i} className="p-3 rounded-lg bg-gray-50 hover:bg-blue-50 cursor-pointer transition-colors border border-transparent hover:border-blue-100">
                      <p className="text-sm font-medium text-gray-800 truncate">关于 IF2312 的后续走势分析...</p>
                      <p className="text-xs text-gray-400 mt-1">2023-11-2{i} 14:30</p>
                   </div>
                 ))}
              </div>
           </div>
        </div>
      </div>
    </MainLayout>
  )
}

