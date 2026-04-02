/**
 * 快速使用说明页面。
 *
 * 面向零代码基础用户，用通俗语言介绍如何注册、浏览信号、搜索、收藏、
 * 账户中心及管理员相关操作。无需登录即可阅读。
 */

import { Link } from 'react-router-dom'
import { isAuthenticated } from '../services/authService'

/** 每个教程章节的数据。 */
interface Section {
  /** 章节标题。 */
  title: string
  /** 章节内容（段落或步骤列表）。 */
  content: React.ReactNode
}

/**
 * 快速使用说明页面。
 *
 * @returns JSX 元素。
 */
export default function Guide() {
  /** 是否已登录，用于显示「进入首页」或「去登录」。 */
  const loggedIn = isAuthenticated()

  /** 教程章节列表，按阅读顺序排列。 */
  const sections: Section[] = [
    {
      title: '一、注册与登录',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            第一次使用需要先<strong>注册账号</strong>，之后每次打开网站时<strong>登录</strong>即可。
          </p>
          <ol className="list-decimal list-inside space-y-2 text-gray-700 ml-2">
            <li>在登录页点击「<strong>去注册</strong>」进入注册页。</li>
            <li>填写手机号（必填）、密码，邮箱和昵称可以选填。</li>
            <li>注册成功后会自动跳转到登录页，用刚才的账号密码登录。</li>
            <li>以后每次打开网站：输入手机号或邮箱、密码，点击「登录」。</li>
            <li>退出时点击页面右上角「退出」即可。</li>
          </ol>
        </>
      ),
    },
    {
      title: '二、主页：怎么看信号',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            登录后会进入<strong>主页（仪表盘）</strong>，这里会显示所有已发布的<strong>交易信号</strong>。
          </p>
          <p className="mb-2 text-gray-700 leading-relaxed">
            每个信号卡片上通常能看到：
          </p>
          <ul className="list-disc list-inside space-y-1 text-gray-700 ml-2 mb-3">
            <li><strong>合约名称</strong>：例如某个期货品种。</li>
            <li><strong>方向</strong>：做多或做空。</li>
            <li><strong>现价</strong>：系统会定时更新，方便您对比。</li>
            <li><strong>止损 / 止盈</strong>：策略里建议的止损价和止盈价。</li>
          </ul>
          <p className="text-gray-700 leading-relaxed">
            想了解某个信号的详细说明，<strong>点击该卡片</strong>即可进入详情页。
          </p>
        </>
      ),
    },
    {
      title: '三、搜索合约',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            在左侧菜单点击「<strong>搜索合约</strong>」进入搜索页。
          </p>
          <ol className="list-decimal list-inside space-y-2 text-gray-700 ml-2">
            <li>在搜索框里输入您关心的品种或关键词（例如合约代码、名称）。</li>
            <li>系统会列出与关键词相关的合约或信号。</li>
            <li>点击某一项即可查看该信号的详情。</li>
          </ol>
        </>
      ),
    },
    {
      title: '四、查看信号详情与收藏',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            在主页或搜索结果里<strong>点击某个信号</strong>，会打开<strong>信号详情页</strong>。
          </p>
          <p className="mb-2 text-gray-700 leading-relaxed">
            详情页里可以看到：
          </p>
          <ul className="list-disc list-inside space-y-1 text-gray-700 ml-2 mb-3">
            <li>该合约的<strong>K 线图</strong>（日线），方便看走势。</li>
            <li>当前价、止损价、止盈价、方向等。</li>
            <li>发布者写的<strong>正文说明</strong>（策略思路、注意事项等）。</li>
          </ul>
          <p className="mb-2 text-gray-700 leading-relaxed">
            如果您觉得这个信号有用，可以点击「<strong>收藏</strong>」，以后在「查看账户」里的「收藏」列表中就能快速找到。
          </p>
          <p className="text-gray-700 leading-relaxed">
            您浏览过的信号也会自动记录在「<strong>浏览历史</strong>」里，方便回顾。
          </p>
        </>
      ),
    },
    {
      title: '五、账户中心：收藏、历史与我的内容',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            在左侧菜单点击「<strong>查看账户</strong>」进入账户中心。这里用<strong>标签页</strong>分成几块：
          </p>
          <ul className="list-disc list-inside space-y-1 text-gray-700 ml-2">
            <li><strong>收藏</strong>：您收藏过的信号列表，点击可再次进入详情。</li>
            <li><strong>浏览历史</strong>：您最近看过的信号，方便回溯。</li>
            <li><strong>我的帖子</strong>：您自己发布过的信号（若有）。</li>
            <li><strong>草稿</strong>：未发布完、保存为草稿的内容，可继续编辑或发布。</li>
          </ul>
          <p className="mt-3 text-gray-700 leading-relaxed">
            普通用户主要会用到「收藏」和「浏览历史」；若您有发布权限，会多出「我的帖子」和「草稿」。
          </p>
        </>
      ),
    },
    {
      title: '六、管理员：编辑与删除信号',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            如果您是<strong>管理员</strong>，可以在<strong>信号详情页</strong>底部看到「<strong>编辑帖子</strong>」「<strong>删除帖子</strong>」等按钮。
          </p>
          <ol className="list-decimal list-inside space-y-2 text-gray-700 ml-2">
            <li>打开要修改的信号详情页，滚动到页面底部。</li>
            <li>点击「编辑帖子」会进入编辑页，可修改标题、止损、止盈、方向、正文等；现价一般为系统自动更新，通常不能手动改。</li>
            <li>修改完成后保存即可。若不再需要该信号，可点击「删除帖子」进行删除。</li>
          </ol>
        </>
      ),
    },
    {
      title: '七、管理员：用户管理（仅超级管理员）',
      content: (
        <>
          <p className="mb-3 text-gray-700 leading-relaxed">
            只有<strong>超级管理员</strong>在「查看账户」里会多出一个「<strong>用户管理</strong>」标签。
          </p>
          <p className="mb-2 text-gray-700 leading-relaxed">
            在这里可以：
          </p>
          <ul className="list-disc list-inside space-y-1 text-gray-700 ml-2">
            <li>查看所有用户列表。</li>
            <li>新增用户（填写手机号、密码、角色等）。</li>
            <li>编辑用户（修改昵称、角色、是否启用等）。</li>
            <li>删除或禁用用户。</li>
          </ul>
        </>
      ),
    },
    {
      title: '八、常见问题',
      content: (
        <>
          <ul className="space-y-2 text-gray-700">
            <li>
              <strong>忘记密码？</strong> 请联系管理员重置，或根据站点提供的「找回密码」入口操作（若有）。
            </li>
            <li>
              <strong>登录失败？</strong> 请确认手机号/邮箱和密码是否正确，注意区分大小写；若账号被禁用，需联系管理员。
            </li>
            <li>
              <strong>页面打不开或一直转圈？</strong> 请检查网络是否正常；若为手机访问，可尝试切换到 WiFi 或换个浏览器再试。
            </li>
            <li>
              <strong>看不到「编辑帖子」？</strong> 该功能仅对管理员开放；若您应是管理员却看不到，请联系超级管理员检查您的角色。
            </li>
          </ul>
        </>
      ),
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部栏：不依赖 MainLayout，方便未登录用户直接看教程 */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">快速使用说明</h1>
          {loggedIn ? (
            <Link
              to="/dashboard"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              进入首页
            </Link>
          ) : (
            <Link
              to="/login"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              去登录
            </Link>
          )}
        </div>
      </header>

      {/* 教程正文：单列、易读，适合零基础用户 */}
      <main className="max-w-3xl mx-auto px-4 py-8 pb-16">
        <p className="text-gray-600 mb-8 leading-relaxed">
          本说明面向<strong>没有任何编程或技术背景</strong>的用户，按步骤即可完成注册、浏览信号、搜索、收藏和账户管理。遇到问题可先看文末「常见问题」。
        </p>

        {sections.map((section, index) => (
          <section
            key={index}
            className="mb-10 p-6 bg-white rounded-xl border border-gray-200 shadow-sm"
          >
            <h2 className="text-lg font-bold text-gray-900 mb-4 border-b border-gray-100 pb-2">
              {section.title}
            </h2>
            <div className="text-gray-700">{section.content}</div>
          </section>
        ))}

        <p className="text-center text-gray-500 text-sm mt-8">
          祝您使用顺利。如需更多帮助，请联系站点管理员。
        </p>
      </main>
    </div>
  )
}
