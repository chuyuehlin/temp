Highcharts.getJSON('./chartdata/1301', function (data) {
    // Create the chart
    Highcharts.stockChart('chart5', {
  
  
      rangeSelector: {
        selected: 1
      },
  
      title: {
        text: '台塑 Stock Price'
      },
  
      series: [{
        name: '台塑',
        data: data,
        tooltip: {
          valueDecimals: 2
        }
      }]
    });
  });