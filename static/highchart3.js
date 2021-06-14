Highcharts.getJSON('./chartdata/1203', function (data) {
    // Create the chart
    Highcharts.stockChart('chart3', {
  
  
      rangeSelector: {
        selected: 1
      },
  
      title: {
        text: '味王 Stock Price'
      },
  
      series: [{
        name: '味王',
        data: data,
        tooltip: {
          valueDecimals: 2
        }
      }]
    });
  });