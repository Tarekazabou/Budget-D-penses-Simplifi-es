import { Pie } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const DashboardChart = ({ data }) => {
  // Couleurs pour le graphique
  const colors = [
    '#3B82F6', // blue-500
    '#EF4444', // red-500
    '#10B981', // green-500
    '#F59E0B', // yellow-500
    '#8B5CF6', // purple-500
    '#EC4899', // pink-500
    '#14B8A6', // teal-500
    '#F97316', // orange-500
    '#6366F1', // indigo-500
    '#84CC16', // lime-500
  ]

  const chartData = {
    labels: data.map(item => item.category),
    datasets: [
      {
        data: data.map(item => item.amount),
        backgroundColor: colors.slice(0, data.length),
        borderColor: colors.slice(0, data.length).map(color => color + '80'),
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.parsed
            const total = context.dataset.data.reduce((sum, val) => sum + val, 0)
            const percentage = ((value / total) * 100).toFixed(1)
            return `${context.label}: ${value.toFixed(2)}€ (${percentage}%)`
          },
        },
      },
    },
  }

  return (
    <div className="relative h-80">
      <Pie data={chartData} options={options} />
    </div>
  )
}

export default DashboardChart