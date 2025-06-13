'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import { useSidebar } from '../context/SidebarContext'

export default function Navigation() {
  const pathname = usePathname()
  const { isOpen, toggleSidebar } = useSidebar()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-primary-600 to-primary-800 text-white shadow-lg">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo and Name */}
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleSidebar}
              className="rounded-lg p-2 text-primary-100 hover:bg-white/10 hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-white/20"
              aria-label={isOpen ? 'Close sidebar' : 'Open sidebar'}
            >
              {isOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center"
            >
              <Link href="/" className="flex items-center space-x-2">
                <span className="text-2xl font-bold tracking-tight">
                  <span className="text-3xl font-bold">सुविधा.in</span>
                </span>
              </Link>
            </motion.div>
          </div>

          {/* Navigation Links */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-4"
          >
            <Link
              href="/"
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                pathname === '/'
                  ? 'bg-white/10 text-white'
                  : 'text-primary-100 hover:bg-white/5 hover:text-white'
              }`}
            >
              Chat
            </Link>
            <Link
              href="/about"
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                pathname === '/about'
                  ? 'bg-white/10 text-white'
                  : 'text-primary-100 hover:bg-white/5 hover:text-white'
              }`}
            >
              About
            </Link>
          </motion.div>
        </div>
      </div>
    </nav>
  )
} 