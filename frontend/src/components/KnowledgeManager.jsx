import React, { useState, useEffect } from 'react'
import { Plus, Trash2, Edit2, Search, Loader } from 'lucide-react'
import { knowledgeAPI } from '../api'

const KnowledgeManager = () => {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category: 'general',
    tags: '',
    source: '',
  })

  useEffect(() => {
    fetchEntries()
  }, [])

  const fetchEntries = async () => {
    setLoading(true)
    try {
      const response = await knowledgeAPI.getAllEntries()
      setEntries(response.data)
      setError('')
    } catch (err) {
      setError('Failed to fetch knowledge entries')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchEntries()
      return
    }

    setLoading(true)
    try {
      const response = await knowledgeAPI.search(searchQuery)
      setEntries(response.data)
      setError('')
    } catch (err) {
      setError('Failed to search knowledge entries')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.title.trim() || !formData.content.trim()) {
      setError('Title and content are required')
      return
    }

    setLoading(true)
    try {
      const data = {
        ...formData,
        tags: formData.tags.split(',').map((tag) => tag.trim()).filter(Boolean),
      }

      if (editingId) {
        await knowledgeAPI.updateEntry(editingId, data)
        setEditingId(null)
      } else {
        await knowledgeAPI.addEntry(data)
      }

      setFormData({
        title: '',
        content: '',
        category: 'general',
        tags: '',
        source: '',
      })
      setShowForm(false)
      setError('')
      await fetchEntries()
    } catch (err) {
      setError('Failed to save knowledge entry')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      setLoading(true)
      try {
        await knowledgeAPI.deleteEntry(id)
        await fetchEntries()
        setError('')
      } catch (err) {
        setError('Failed to delete knowledge entry')
        console.error('Error:', err)
      } finally {
        setLoading(false)
      }
    }
  }

  const handleEdit = (entry) => {
    setFormData({
      title: entry.title,
      content: entry.content,
      category: entry.category,
      tags: entry.tags?.join(', ') || '',
      source: entry.source || '',
    })
    setEditingId(entry.id)
    setShowForm(true)
  }

  const handleCancel = () => {
    setFormData({
      title: '',
      content: '',
      category: 'general',
      tags: '',
      source: '',
    })
    setEditingId(null)
    setShowForm(false)
  }

  const filteredEntries = entries.filter((entry) => {
    const query = searchQuery.toLowerCase()
    return (
      entry.title.toLowerCase().includes(query) ||
      entry.content.toLowerCase().includes(query)
    )
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Knowledge Base</h1>
          <p className="text-gray-400">Manage your personal knowledge entries</p>
        </div>

        {/* Search and Add */}
        <div className="mb-8 space-y-4">
          <div className="flex gap-2">
            <div className="flex-1 flex gap-2">
              <input
                type="text"
                placeholder="Search knowledge base..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1 bg-gray-700 text-white placeholder-gray-400 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <button
                onClick={handleSearch}
                className="bg-primary hover:bg-red-700 text-white rounded-lg px-4 py-2 flex items-center gap-2 transition-colors"
              >
                <Search className="w-4 h-4" />
                Search
              </button>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              className="bg-green-600 hover:bg-green-700 text-white rounded-lg px-4 py-2 flex items-center gap-2 transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add Entry
            </button>
          </div>

          {error && (
            <div className="bg-red-900 text-red-100 p-3 rounded-lg flex items-center gap-2">
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Form */}
        {showForm && (
          <div className="bg-gray-800 rounded-lg p-6 mb-8 border border-gray-700">
            <h2 className="text-2xl font-bold mb-4">
              {editingId ? 'Edit Entry' : 'Add New Entry'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Entry title"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Content</label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary h-32"
                  placeholder="Entry content"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Category</label>
                  <select
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <option>general</option>
                    <option>technical</option>
                    <option>business</option>
                    <option>personal</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Tags (comma-separated)</label>
                  <input
                    type="text"
                    value={formData.tags}
                    onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
                    className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="tag1, tag2, tag3"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Source (optional)</label>
                <input
                  type="text"
                  value={formData.source}
                  onChange={(e) => setFormData({ ...formData, source: e.target.value })}
                  className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="Source URL or reference"
                />
              </div>

              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={handleCancel}
                  className="bg-gray-700 hover:bg-gray-600 text-white rounded-lg px-4 py-2 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-green-600 hover:bg-green-700 text-white rounded-lg px-4 py-2 flex items-center gap-2 disabled:opacity-50 transition-colors"
                >
                  {loading ? (
                    <Loader className="w-4 h-4 animate-spin" />
                  ) : (
                    <span>{editingId ? 'Update' : 'Add'}</span>
                  )}
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Entries List */}
        <div className="space-y-4">
          {loading && !showForm ? (
            <div className="flex justify-center items-center py-8">
              <Loader className="w-6 h-6 animate-spin" />
            </div>
          ) : filteredEntries.length === 0 ? (
            <div className="bg-gray-800 rounded-lg p-8 text-center border border-gray-700">
              <p className="text-gray-400">
                {searchQuery
                  ? 'No entries found matching your search'
                  : 'No knowledge entries yet. Add one to get started!'}
              </p>
            </div>
          ) : (
            filteredEntries.map((entry) => (
              <div
                key={entry.id}
                className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-primary transition-colors"
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold mb-1">{entry.title}</h3>
                    <p className="text-gray-400 mb-2 line-clamp-2">{entry.content}</p>
                    <div className="flex gap-2 flex-wrap">
                      <span className="bg-primary bg-opacity-20 text-primary text-xs px-2 py-1 rounded">
                        {entry.category}
                      </span>
                      {entry.tags?.map((tag) => (
                        <span
                          key={tag}
                          className="bg-gray-700 text-gray-300 text-xs px-2 py-1 rounded"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <button
                      onClick={() => handleEdit(entry)}
                      className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-3 py-2 flex items-center gap-1 transition-colors"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(entry.id)}
                      className="bg-red-600 hover:bg-red-700 text-white rounded-lg px-3 py-2 flex items-center gap-1 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default KnowledgeManager
