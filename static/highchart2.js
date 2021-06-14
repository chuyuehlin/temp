Highcharts.getJSON('./chartdata/1234', function (data) {
    // Create the chart
    Highcharts.stockChart('chart2', {
  
  
      rangeSelector: {
        selected: 1
      },
  
      title: {
        text: '黑松 Stock Price'
      },
  
      series: [{
        name: '黑松',
        data: data,
        tooltip: {
          valueDecimals: 2
        }
      }]
    });
  });