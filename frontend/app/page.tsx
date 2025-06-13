'use client'

import { motion } from 'framer-motion'
import ChatInterface from './components/ChatInterface'
import Navigation from './components/Navigation'
import Sidebar from './components/Sidebar'
import { ArrowRightIcon, DocumentTextIcon, ChatBubbleLeftRightIcon, BookOpenIcon } from '@heroicons/react/24/outline'
import { useSidebar } from './context/SidebarContext'

export default function Home() {
  const { isOpen } = useSidebar()

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <Navigation />
      <Sidebar />
      
      {/* Main Content */}
      <main className={`transition-all duration-300 ${isOpen ? 'pl-80' : 'pl-0'}`}>
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-gradient-to-r from-primary-600 to-primary-800 text-white pt-24">
          <div className="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" />
          <div className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
                GFR & PM Assistant
              </h1>
              <p className="mt-6 text-lg sm:text-xl text-primary-100 max-w-2xl mx-auto">
                Your intelligent assistant for General Financial Rules (GFR) 2017 and
                Procurement Manual (PM) 2025, powered by advanced AI technology
              </p>
            </motion.div>

            {/* Feature Highlights */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3"
            >
              <div className="relative rounded-2xl bg-white/10 p-6 backdrop-blur-sm">
                <DocumentTextIcon className="h-8 w-8 text-primary-200" />
                <h3 className="mt-4 text-lg font-semibold">Smart Document Processing</h3>
                <p className="mt-2 text-primary-100">
                  Advanced extraction and organization of rules from GFR and PM documents
                </p>
              </div>
              <div className="relative rounded-2xl bg-white/10 p-6 backdrop-blur-sm">
                <ChatBubbleLeftRightIcon className="h-8 w-8 text-primary-200" />
                <h3 className="mt-4 text-lg font-semibold">Intelligent Chat</h3>
                <p className="mt-2 text-primary-100">
                  Natural conversations with accurate citations and context-aware responses
                </p>
              </div>
              <div className="relative rounded-2xl bg-white/10 p-6 backdrop-blur-sm">
                <BookOpenIcon className="h-8 w-8 text-primary-200" />
                <h3 className="mt-4 text-lg font-semibold">Comprehensive Knowledge</h3>
                <p className="mt-2 text-primary-100">
                  Access to both GFR 2017 and PM 2025 with proper citations and references
                </p>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Chat Section */}
        <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card shadow-lg"
          >
            <div className="card-header bg-gradient-to-r from-primary-600 to-primary-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-white">Chat Assistant</h2>
                <a
                  href="/about"
                  className="inline-flex items-center space-x-1 text-sm text-primary-100 hover:text-white transition-colors"
                >
                  <span>Learn more</span>
                  <ArrowRightIcon className="h-4 w-4" />
                </a>
              </div>
            </div>
            <div className="card-body p-0">
              <ChatInterface />
            </div>
          </motion.div>
        </section>
      </main>
    </div>
  )
} 