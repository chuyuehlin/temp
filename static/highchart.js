Highcharts.getJSON('./chartdata/1101', function (data) {
  // Create the chart
  Highcharts.stockChart('chart', {


    rangeSelector: {
      selected: 1
    },

    title: {
      text: '台泥 Stock Price'
    },

    series: [{
      name: '台泥',
      data: data,
      tooltip: {
        valueDecimals: 2
      }
    }]
  });
});