import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Configuration de base d'axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les erreurs d'authentification
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Services d'authentification
export const authService = {
  async login(email, password) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
    }
    
    return response.data
  },

  async register(email, password) {
    const response = await api.post('/auth/register', {
      email,
      password,
    })
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  getCurrentUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  },
}

// Services pour les transactions
export const transactionService = {
  async getTransactions(params = {}) {
    const response = await api.get('/transactions', { params })
    return response.data
  },

  async createTransaction(transaction) {
    const response = await api.post('/transactions', transaction)
    return response.data
  },

  async updateTransaction(id, transaction) {
    const response = await api.put(`/transactions/${id}`, transaction)
    return response.data
  },

  async deleteTransaction(id) {
    await api.delete(`/transactions/${id}`)
  },

  async getTransaction(id) {
    const response = await api.get(`/transactions/${id}`)
    return response.data
  },
}

// Services pour le tableau de bord
export const dashboardService = {
  async getBalance(period = 'monthly') {
    const response = await api.get('/dashboard/balance', {
      params: { period }
    })
    return response.data
  },

  async getExpensesByCategory(period = 'monthly') {
    const response = await api.get('/dashboard/expenses-by-category', {
      params: { period }
    })
    return response.data
  },

  async getSummary(period = 'monthly') {
    const response = await api.get('/dashboard/summary', {
      params: { period }
    })
    return response.data
  },
}

// Services pour les budgets (à implémenter plus tard)
export const budgetService = {
  async getBudgets() {
    const response = await api.get('/budgets')
    return response.data
  },

  async createBudget(budget) {
    const response = await api.post('/budgets', budget)
    return response.data
  },
}

export default api