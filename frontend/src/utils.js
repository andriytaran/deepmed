export const formatChartNumber = (tooltipItem, data) => {
  const value = data.datasets[0].data[tooltipItem.index]
  const label = data.labels[tooltipItem.index]
  const percentage = Math.round(value * 100) / 100
  return `${label} ${percentage}%`
}
