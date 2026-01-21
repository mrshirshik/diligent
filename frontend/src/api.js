import axios from 'axios'

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const chatAPI = {
  sendMessage: (query, conversationHistory = []) =>
    api.post('/chat', {
      query,
      conversation_history: conversationHistory,
    }),

  getHealth: () => api.get('/health'),
}

export const knowledgeAPI = {
  getAllEntries: () => api.get('/knowledge'),

  getEntry: (id) => api.get(`/knowledge/${id}`),

  addEntry: (data) => api.post('/knowledge', data),

  updateEntry: (id, data) => api.put(`/knowledge/${id}`, data),

  deleteEntry: (id) => api.delete(`/knowledge/${id}`),

  search: (query, topK = 5) =>
    api.post('/search', {
      query,
      top_k: topK,
    }),
}

export default api
