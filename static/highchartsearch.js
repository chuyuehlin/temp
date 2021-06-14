Highcharts.getJSON('./chartdata/' + document.getElementById('Stock').value, function (data) {
  // Create the chart
  Highcharts.stockChart('chart7', {


    rangeSelector: {
      selected: 1
    },

    title: {
      text: stockname + ' Stock Price'
    },

    series: [{
      name: stockname,
      data: data,
      tooltip: {
        valueDecimals: 2
      }
    }]
  });
});