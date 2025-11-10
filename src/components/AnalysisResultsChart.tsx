import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface DataPoint {
  label: string;
  value: number;
}

interface AnalysisResultsChartProps {
  data: DataPoint[];
}

const AnalysisResultsChart: React.FC<AnalysisResultsChartProps> = ({ data }) => {
  const chartData = {
    labels: data.map((item: DataPoint) => item.label),
    datasets: [
      {
        label: 'Analysis Results',
        data: data.map((item: DataPoint) => item.value),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Analysis Results',
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default AnalysisResultsChart;