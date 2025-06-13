'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { DocumentArrowDownIcon, BookOpenIcon, DocumentTextIcon } from '@heroicons/react/24/outline'
import { useSidebar } from '../context/SidebarContext'

export default function Sidebar() {
  const { isOpen } = useSidebar()
  const manuals = [
    {
      title: 'General Financial Rules (GFR) 2017',
      description: 'The General Financial Rules (GFR) 2017 is a comprehensive document that contains rules and orders for regulating the financial matters of the Government of India. It covers various aspects of financial management including budgeting, accounting, procurement, and audit procedures.',
      icon: DocumentTextIcon,
      downloadUrl: '/documents/gfr-2017.pdf',
      size: '2.4 MB',
      lastUpdated: 'March 2017'
    },
    {
      title: 'Procurement Manual (PM) 2025',
      description: 'The Procurement Manual 2025 provides detailed guidelines and procedures for procurement of goods, services, and works by government departments. It includes best practices, standard procedures, and regulatory requirements for transparent and efficient procurement processes.',
      icon: BookOpenIcon,
      downloadUrl: '/documents/pm-2025.pdf',
      size: '3.1 MB',
      lastUpdated: 'January 2025'
    }
  ]

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.aside
          initial={{ opacity: 0, x: -320 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -320 }}
          transition={{ type: 'spring', damping: 20 }}
          className="fixed left-0 top-16 h-[calc(100vh-4rem)] w-80 overflow-y-auto border-r border-gray-200 bg-white p-6"
        >
          <div className="space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Document Downloads</h2>
              <p className="mt-1 text-sm text-gray-600">
                Access the official documents for detailed information
              </p>
            </div>

            <div className="space-y-4">
              {manuals.map((manual) => (
                <div
                  key={manual.title}
                  className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
                >
                  <div className="flex items-start space-x-3">
                    <manual.icon className="h-6 w-6 text-primary-600" />
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{manual.title}</h3>
                      <p className="mt-1 text-sm text-gray-600">{manual.description}</p>
                      <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
                        <span>Size: {manual.size}</span>
                        <span>Updated: {manual.lastUpdated}</span>
                      </div>
                      <a
                        href={manual.downloadUrl}
                        className="mt-3 inline-flex items-center space-x-1 text-sm font-medium text-primary-600 hover:text-primary-700"
                        download
                      >
                        <DocumentArrowDownIcon className="h-4 w-4" />
                        <span>Download PDF</span>
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="rounded-lg bg-primary-50 p-4">
              <h3 className="font-medium text-primary-900">About the Documents</h3>
              <p className="mt-2 text-sm text-primary-700">
                These documents are essential resources for understanding government financial procedures
                and procurement processes. They are regularly updated to reflect current regulations
                and best practices.
              </p>
              <div className="mt-4 space-y-2 text-sm text-primary-600">
                <p>• Official government documents</p>
                <p>• Updated with latest amendments</p>
                <p>• Comprehensive guidelines</p>
                <p>• Standard procedures</p>
              </div>
            </div>

            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">
              <h3 className="font-medium text-gray-900">Need Help?</h3>
              <p className="mt-2 text-sm text-gray-600">
                Use our AI assistant to quickly find information from these documents.
                Just ask your question in the chat interface!
              </p>
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  )
} 