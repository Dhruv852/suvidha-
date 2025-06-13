'use client'

import { motion } from 'framer-motion'
import Navigation from '../components/Navigation'
import Sidebar from '../components/Sidebar'
import { useSidebar } from '../context/SidebarContext'
import { DocumentTextIcon, ChatBubbleLeftRightIcon, BookOpenIcon, LightBulbIcon, ShieldCheckIcon, EnvelopeIcon } from '@heroicons/react/24/outline'

export default function About() {
  const { isOpen } = useSidebar()

  const features = [
    {
      icon: DocumentTextIcon,
      title: 'Smart Document Processing',
      description: 'Advanced extraction and organization of rules from GFR and PM documents using state-of-the-art AI technology.',
    },
    {
      icon: ChatBubbleLeftRightIcon,
      title: 'Intelligent Chat Interface',
      description: 'Natural language conversations with accurate citations and context-aware responses powered by advanced language models.',
    },
    {
      icon: BookOpenIcon,
      title: 'Comprehensive Knowledge Base',
      description: 'Access to both GFR 2017 and PM 2025 with proper citations and references, ensuring accurate and up-to-date information.',
    },
    {
      icon: LightBulbIcon,
      title: 'Smart Context Understanding',
      description: 'The system maintains conversation context and provides relevant information based on the user\'s query history.',
    },
    {
      icon: ShieldCheckIcon,
      title: 'Accurate Citations',
      description: 'Every response includes proper citations from both GFR and PM documents, ensuring transparency and reliability.',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <Navigation />
      <Sidebar />
      
      {/* Main Content */}
      <main className={`transition-all duration-300 ${isOpen ? 'pl-80' : 'pl-0'}`}>
        {/* Header */}
        <header className="relative overflow-hidden bg-gradient-to-r from-primary-600 to-primary-800 text-white pt-24">
          <div className="absolute inset-0 bg-grid-white/10 [mask-image:linear-gradient(0deg,white,rgba(255,255,255,0.6))]" />
          <div className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
                About GFR & PM Assistant
              </h1>
              <p className="mt-6 text-lg sm:text-xl text-primary-100 max-w-3xl mx-auto">
                An intelligent AI-powered assistant designed to help users navigate and understand
                the General Financial Rules (GFR) 2017 and Procurement Manual (PM) 2025
              </p>
            </motion.div>
          </div>
        </header>

        {/* Content */}
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          {/* Features Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3"
          >
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.1 }}
                className="card hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  <feature.icon className="h-8 w-8 text-primary-600" />
                  <h3 className="mt-4 text-lg font-semibold text-gray-900">{feature.title}</h3>
                  <p className="mt-2 text-gray-600">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>

          {/* How It Works Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mt-16 card"
          >
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">How It Works</h2>
              <div className="prose prose-primary max-w-none">
                <p>
                  The GFR & PM Assistant uses advanced natural language processing and machine learning
                  techniques to understand and respond to user queries about financial rules and procurement
                  procedures. The system processes both GFR 2017 and PM 2025 documents to create a
                  comprehensive knowledge base that can be queried through natural conversation.
                </p>
                <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                  <div className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                      1
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">Ask Your Question</h3>
                      <p className="mt-2 text-gray-600">
                        Type your question about GFR or PM rules in natural language
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                      2
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">AI Processing</h3>
                      <p className="mt-2 text-gray-600">
                        Our AI analyzes your question and searches through the relevant documents
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-100 text-primary-700">
                      3
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">Get Detailed Response</h3>
                      <p className="mt-2 text-gray-600">
                        Receive a comprehensive answer with proper citations and context
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Contact Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-16 card bg-primary-50"
          >
            <div className="p-6">
              <h2 className="text-2xl font-semibold text-primary-900">Need Help?</h2>
              <p className="mt-4 text-primary-700">
                If you have any questions or need assistance, please don't hesitate to contact us.
                Our team is here to help you make the most of the GFR & PM Assistant.
              </p>
              <div className="mt-6">
                <a
                  href="mailto:gfrpmassistant@gmail.com"
                  className="inline-flex items-center gap-2 px-6 py-3 text-base font-medium text-white bg-primary-600 rounded-lg shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200 transform hover:scale-105 hover:shadow-lg active:scale-95"
                >
                  <EnvelopeIcon className="w-5 h-5" />
                  Contact Support
                </a>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  )
} 