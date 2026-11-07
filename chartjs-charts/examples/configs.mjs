// Original illustrative data. Requires Chart.js 4.x and a sized canvas container.
export const exampleKinds = ['bar', 'line', 'scatter', 'doughnut', 'stacked', 'mixed'];

export function createExampleConfig(kind = 'bar') {
  const blue = '#2866A0';
  const teal = '#167D71';
  const amber = '#A86809';
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    color: '#24374A',
    plugins: {
      title: { display: true, text: '' },
      legend: { display: false, position: 'bottom' },
    },
  };
  const axis = (text) => ({ title: { display: true, text } });
  const countAxis = (text) => ({ ...axis(text), beginAtZero: true, ticks: { precision: 0 } });
  const config = { type: 'bar', data: { labels: [], datasets: [] }, options };

  switch (kind) {
    case 'bar':
      options.plugins.title.text = 'Requests by queue (illustrative)';
      config.data.labels = ['General', 'Billing', 'Technical'];
      config.data.datasets = [{ label: 'Requests', data: [28, 19, 16], backgroundColor: blue }];
      options.scales = { x: axis('Queue'), y: countAxis('Requests') };
      break;
    case 'line':
      config.type = 'line';
      options.plugins.title.text = 'Monthly throughput with a missing value (illustrative)';
      config.data.labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May'];
      config.data.datasets = [{
        label: 'Completed items', data: [18, 24, null, 21, 29],
        borderColor: teal, backgroundColor: teal, pointRadius: 4,
        fill: false, spanGaps: false, tension: 0,
      }];
      options.scales = { x: axis('Month (ordered categories)'), y: countAxis('Completed items') };
      break;
    case 'scatter':
      config.type = 'scatter';
      options.plugins.title.text = 'Effort and duration (illustrative)';
      config.data.datasets = [{
        label: 'Tasks', data: [{ x: 2, y: 3 }, { x: 4, y: 7 }, { x: 7, y: 5 }, { x: 10, y: 12 }],
        backgroundColor: blue, pointRadius: 5,
      }];
      options.scales = { x: { ...axis('Effort (hours)'), type: 'linear', beginAtZero: true }, y: { ...axis('Duration (days)'), beginAtZero: true } };
      break;
    case 'doughnut':
      config.type = 'doughnut';
      options.plugins.title.text = 'Request composition (illustrative)';
      options.plugins.legend.display = true;
      config.data.labels = ['General', 'Billing', 'Technical'];
      config.data.datasets = [{ label: 'Requests', data: [28, 19, 16], backgroundColor: [blue, teal, amber], borderWidth: 2, borderColor: '#FFFFFF' }];
      break;
    case 'stacked':
      options.indexAxis = 'y';
      options.plugins.title.text = 'Queue workload by status (illustrative)';
      options.plugins.legend.display = true;
      config.data.labels = ['General', 'Billing', 'Technical'];
      config.data.datasets = [
        { label: 'Open', data: [12, 8, 7], backgroundColor: blue, stack: 'workload' },
        { label: 'Closed', data: [16, 11, 9], backgroundColor: teal, stack: 'workload' },
      ];
      options.scales = { x: { ...countAxis('Requests'), stacked: true }, y: { ...axis('Queue'), stacked: true } };
      break;
    case 'mixed':
      options.plugins.title.text = 'Actual and target throughput (illustrative)';
      options.plugins.legend.display = true;
      config.data.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
      config.data.datasets = [
        { type: 'bar', label: 'Actual', data: [18, 24, 21, 29], backgroundColor: blue, order: 2 },
        { type: 'line', label: 'Target', data: [23, 23, 23, 23], borderColor: amber, backgroundColor: amber, borderDash: [6, 4], pointStyle: 'rectRot', pointRadius: 4, fill: false, order: 1 },
      ];
      options.scales = { x: axis('Week'), y: countAxis('Completed items') };
      break;
    default:
      throw new RangeError(`Unknown example kind: ${kind}`);
  }
  return config;
}
