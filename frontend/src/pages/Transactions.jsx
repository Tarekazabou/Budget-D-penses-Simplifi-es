import { useState, useEffect } from 'react'
import { transactionService } from '../services/api'
import { Plus, Search, Filter, Edit, Trash2 } from 'lucide-react'
import TransactionForm from '../components/TransactionForm'
import LoadingSpinner from '../components/LoadingSpinner'

const Transactions = () => {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingTransaction, setEditingTransaction] = useState(null)
  const [filters, setFilters] = useState({
    type: '',
    category: '',
    search: '',
  })

  useEffect(() => {
    fetchTransactions()
  }, [filters])

  const fetchTransactions = async () => {
    try {
      setLoading(true)
      const params = {}
      if (filters.type) params.transaction_type = filters.type
      if (filters.category) params.category = filters.category
      
      const data = await transactionService.getTransactions(params)
      
      // Filtrer par recherche côté client
      let filteredData = data
      if (filters.search) {
        filteredData = data.filter(transaction => 
          transaction.description?.toLowerCase().includes(filters.search.toLowerCase()) ||
          transaction.category.toLowerCase().includes(filters.search.toLowerCase())
        )
      }
      
      setTransactions(filteredData)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement des transactions')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette transaction ?')) {
      try {
        await transactionService.deleteTransaction(id)
        await fetchTransactions()
      } catch (err) {
        setError(err.response?.data?.detail || 'Erreur lors de la suppression')
      }
    }
  }

  const handleEdit = (transaction) => {
    setEditingTransaction(transaction)
    setShowForm(true)
  }

  const handleFormClose = () => {
    setShowForm(false)
    setEditingTransaction(null)
    fetchTransactions()
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
    }).format(amount)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR')
  }

  const getCategoryLabel = (category) => {
    const labels = {
      salaire: 'Salaire',
      freelance: 'Freelance',
      investissement: 'Investissement',
      autre_revenu: 'Autre revenu',
      courses: 'Courses',
      loyer: 'Loyer',
      transport: 'Transport',
      utilities: 'Services publics',
      divertissement: 'Divertissement',
      sante: 'Santé',
      education: 'Éducation',
      vetements: 'Vêtements',
      restaurant: 'Restaurant',
      autre_depense: 'Autre dépense',
    }
    return labels[category] || category
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* En-tête */}
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Transactions
            </h2>
          </div>
          <div className="mt-4 flex md:mt-0 md:ml-4">
            <button
              onClick={() => setShowForm(true)}
              className="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <Plus className="h-4 w-4 mr-2" />
              Nouvelle transaction
            </button>
          </div>
        </div>

        {/* Filtres */}
        <div className="mt-6 bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Recherche
                </label>
                <div className="mt-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    className="pl-10 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    placeholder="Rechercher..."
                    value={filters.search}
                    onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Type
                </label>
                <select
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  value={filters.type}
                  onChange={(e) => setFilters({ ...filters, type: e.target.value })}
                >
                  <option value="">Tous les types</option>
                  <option value="income">Revenus</option>
                  <option value="expense">Dépenses</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Catégorie
                </label>
                <select
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  value={filters.category}
                  onChange={(e) => setFilters({ ...filters, category: e.target.value })}
                >
                  <option value="">Toutes les catégories</option>
                  <option value="courses">Courses</option>
                  <option value="loyer">Loyer</option>
                  <option value="transport">Transport</option>
                  <option value="restaurant">Restaurant</option>
                  <option value="salaire">Salaire</option>
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={() => setFilters({ type: '', category: '', search: '' })}
                  className="w-full inline-flex justify-center items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  <Filter className="h-4 w-4 mr-2" />
                  Réinitialiser
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Liste des transactions */}
        <div className="mt-6">
          {loading ? (
            <div className="bg-white shadow rounded-lg p-6">
              <LoadingSpinner />
            </div>
          ) : error ? (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
              {error}
            </div>
          ) : transactions.length === 0 ? (
            <div className="bg-white shadow rounded-lg p-6 text-center">
              <p className="text-gray-500">Aucune transaction trouvée.</p>
            </div>
          ) : (
            <div className="bg-white shadow overflow-hidden sm:rounded-md">
              <ul className="divide-y divide-gray-200">
                {transactions.map((transaction) => (
                  <li key={transaction.transaction_id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <div className={`h-2 w-2 rounded-full ${
                              transaction.type === 'income' ? 'bg-green-400' : 'bg-red-400'
                            }`} />
                          </div>
                          <div className="ml-4">
                            <div className="flex items-center">
                              <p className="text-sm font-medium text-gray-900">
                                {transaction.description || 'Transaction'}
                              </p>
                              <p className="ml-2 text-sm text-gray-500">
                                {getCategoryLabel(transaction.category)}
                              </p>
                            </div>
                            <p className="text-sm text-gray-500">
                              {formatDate(transaction.date)}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center">
                          <p className={`text-sm font-medium ${
                            transaction.type === 'income' ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {transaction.type === 'income' ? '+' : '-'}
                            {formatCurrency(transaction.amount)}
                          </p>
                          <div className="ml-4 flex items-center space-x-2">
                            <button
                              onClick={() => handleEdit(transaction)}
                              className="text-gray-400 hover:text-gray-600"
                            >
                              <Edit className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() => handleDelete(transaction.transaction_id)}
                              className="text-gray-400 hover:text-red-600"
                            >
                              <Trash2 className="h-4 w-4" />
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Modal de formulaire */}
      {showForm && (
        <TransactionForm
          transaction={editingTransaction}
          onClose={handleFormClose}
        />
      )}
    </div>
  )
}

export default Transactions