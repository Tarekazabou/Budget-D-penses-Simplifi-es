import { useState, useEffect } from 'react'
import { dashboardService } from '../services/api'
import { 
  TrendingUp, 
  TrendingDown, 
  Wallet,
  AlertCircle 
} from 'lucide-react'
import DashboardChart from '../components/DashboardChart'
import LoadingSpinner from '../components/LoadingSpinner'

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [period, setPeriod] = useState('monthly')

  useEffect(() => {
    fetchDashboardData()
  }, [period])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const data = await dashboardService.getSummary(period)
      setDashboardData(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement des données')
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
    }).format(amount)
  }

  const getPeriodLabel = (period) => {
    switch (period) {
      case 'weekly':
        return 'Semaine'
      case 'monthly':
        return 'Mois'
      case 'yearly':
        return 'Année'
      default:
        return 'Période'
    }
  }

  if (loading) {
    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <LoadingSpinner />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 mr-2" />
              {error}
            </div>
          </div>
        </div>
      </div>
    )
  }

  const { balance, expenses_by_category } = dashboardData || {}

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* En-tête */}
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              Tableau de bord
            </h2>
          </div>
          <div className="mt-4 flex md:mt-0 md:ml-4">
            <select
              value={period}
              onChange={(e) => setPeriod(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
            >
              <option value="weekly">Semaine</option>
              <option value="monthly">Mois</option>
              <option value="yearly">Année</option>
            </select>
          </div>
        </div>

        {/* Cartes de statistiques */}
        <div className="mt-8">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {/* Revenus */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <TrendingUp className="h-6 w-6 text-green-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Revenus ({getPeriodLabel(period)})
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {formatCurrency(balance?.total_income || 0)}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            {/* Dépenses */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <TrendingDown className="h-6 w-6 text-red-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Dépenses ({getPeriodLabel(period)})
                      </dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {formatCurrency(balance?.total_expenses || 0)}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            {/* Solde */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <Wallet className={`h-6 w-6 ${
                      (balance?.balance || 0) >= 0 ? 'text-blue-400' : 'text-red-400'
                    }`} />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Solde ({getPeriodLabel(period)})
                      </dt>
                      <dd className={`text-lg font-medium ${
                        (balance?.balance || 0) >= 0 ? 'text-green-900' : 'text-red-900'
                      }`}>
                        {formatCurrency(balance?.balance || 0)}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Graphiques */}
        {expenses_by_category && expenses_by_category.length > 0 && (
          <div className="mt-8">
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Répartition des dépenses par catégorie
                </h3>
                <DashboardChart data={expenses_by_category} />
              </div>
            </div>
          </div>
        )}

        {/* Message si pas de données */}
        {(!expenses_by_category || expenses_by_category.length === 0) && (
          <div className="mt-8">
            <div className="bg-white shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <div className="text-center">
                  <Wallet className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">
                    Aucune transaction
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Commencez par ajouter vos premières transactions pour voir vos graphiques.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard