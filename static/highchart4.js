Highcharts.getJSON('./chartdata/1201', function (data) {
    // Create the chart
    Highcharts.stockChart('chart4', {
  
  
      rangeSelector: {
        selected: 1
      },
  
      title: {
        text: '味全 Stock Price'
      },
  
      series: [{
        name: '味全',
        data: data,
        tooltip: {
          valueDecimals: 2
        }
      }]
    });
  });