import './index.css'
import React, { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import KnowledgeManager from './components/KnowledgeManager'
import { MessageCircle, BookOpen } from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="bg-gray-900">
      {activeTab === 'chat' ? (
        <ChatInterface />
      ) : (
        <>
          {/* Tab Navigation */}
          <div className="bg-gradient-to-r from-primary to-red-700 text-white p-4 sticky top-0 z-10">
            <div className="max-w-6xl mx-auto flex gap-4">
              <button
                onClick={() => setActiveTab('chat')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  activeTab === 'chat'
                    ? 'bg-white text-primary'
                    : 'bg-red-700 hover:bg-red-600'
                }`}
              >
                <MessageCircle className="w-5 h-5" />
                Chat
              </button>
              <button
                onClick={() => setActiveTab('knowledge')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                  activeTab === 'knowledge'
                    ? 'bg-white text-primary'
                    : 'bg-red-700 hover:bg-red-600'
                }`}
              >
                <BookOpen className="w-5 h-5" />
                Knowledge Base
              </button>
            </div>
          </div>
          <KnowledgeManager />
        </>
      )}

      {/* Tab Navigation for Chat */}
      {activeTab === 'chat' && (
        <div className="fixed bottom-6 right-6 flex gap-2 z-50">
          <button
            onClick={() => setActiveTab('knowledge')}
            className="bg-primary hover:bg-red-700 text-white rounded-full p-4 shadow-lg transition-colors flex items-center justify-center"
            title="Manage Knowledge Base"
          >
            <BookOpen className="w-6 h-6" />
          </button>
        </div>
      )}
    </div>
  )
}

export default App
