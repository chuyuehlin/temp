Highcharts.getJSON('./chartdata/1218', function (data) {
    // Create the chart
    Highcharts.stockChart('chart6', {
  
  
      rangeSelector: {
        selected: 1
      },
  
      title: {
        text: '泰山 Stock Price'
      },
  
      series: [{
        name: '泰山',
        data: data,
        tooltip: {
          valueDecimals: 2
        }
      }]
    });
  });