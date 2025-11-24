import Sidebar from './Sidebar'
import Header from './Header'

interface MainLayoutProps {
  children: React.ReactNode
  user: any
  onLogout: () => void
}

export default function MainLayout({ children, user, onLogout }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <Header user={user} onLogout={onLogout} />
      
      <main className="pl-64 pt-16 min-h-screen transition-all duration-300">
        <div className="p-6 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  )
}

