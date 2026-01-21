import React, { useState, useRef, useEffect } from 'react'
import { Send, Loader, AlertCircle, CheckCircle } from 'lucide-react'
import { chatAPI } from '../api'

const ChatInterface = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [health, setHealth] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    checkHealth()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const checkHealth = async () => {
    try {
      const response = await chatAPI.getHealth()
      setHealth(response.data)
    } catch (err) {
      setError('Failed to connect to the server')
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()

    if (!input.trim()) return

    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setError('')
    setLoading(true)

    try {
      const response = await chatAPI.sendMessage(input, messages)
      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        sources: response.data.sources,
        confidence: response.data.confidence,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      setError('Failed to get response from the assistant')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary to-red-700 text-white p-6 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Jarvis Assistant</h1>
              <p className="text-red-100 text-sm">Your Personal AI Assistant</p>
            </div>
            {health && (
              <div className="flex items-center gap-2">
                {health.status === 'healthy' ? (
                  <CheckCircle className="w-6 h-6 text-green-300" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-yellow-300" />
                )}
                <span className="text-sm">
                  {health.llm_available && health.embedding_model_available
                    ? 'Ready'
                    : 'Limited Mode'}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 max-w-4xl w-full mx-auto space-y-4">
        {messages.length === 0 && (
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Welcome to Jarvis</h2>
              <p className="text-gray-400">Ask me anything. I'm here to help!</p>
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg ${
                message.role === 'user'
                  ? 'bg-primary text-white'
                  : 'bg-gray-700 text-gray-100'
              }`}
            >
              <p className="break-words">{message.content}</p>

              {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-600">
                  <p className="text-xs font-semibold text-gray-300 mb-2">Sources:</p>
                  <div className="space-y-1">
                    {message.sources.slice(0, 2).map((source, i) => (
                      <p
                        key={i}
                        className="text-xs text-gray-400 truncate hover:text-gray-300"
                      >
                        • {source.metadata?.title || `Source ${i + 1}`}
                      </p>
                    ))}
                  </div>
                  {message.confidence && (
                    <p className="text-xs text-gray-400 mt-2">
                      Confidence: {(message.confidence * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-gray-100 px-4 py-3 rounded-lg flex items-center gap-2">
              <Loader className="w-4 h-4 animate-spin" />
              <span>Thinking...</span>
            </div>
          </div>
        )}

        {error && (
          <div className="flex justify-center">
            <div className="bg-red-900 text-red-100 px-4 py-3 rounded-lg flex items-center gap-2 max-w-md">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-gray-800 border-t border-gray-700 p-6">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSendMessage} className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything..."
              disabled={loading}
              className="flex-1 bg-gray-700 text-white placeholder-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-primary hover:bg-red-700 text-white rounded-lg px-6 py-3 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <Loader className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
