function alerter() {
    alert("Hello");
};

function func(){
    $(function () {
        $('#categorybar').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Order Statistics by Category'
            },
            xAxis: {
                type: 'category',
                labels: {
                    rotation: -45,
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Orders From Category'
                }
            },
            legend: {
                enabled: false
            },
            tooltip: {
                pointFormat: 'Number of Orders: <b>{point.y:f}</b>'
            },
            series: [{
                name: 'Category',
                data: [
                    ['Appetizers', {{ appetizers }}],
                    ['Soups', {{ soups }}],
                    ['Salads', {{ salads }}],
                    ['Kids Menu', {{ kids }}],
                    ['Entrees', {{ entrees }}],
                    ['Breads', {{ breads }}],
                    ['Drinks', {{ drinks }}],
                    ['Desserts', {{ desserts }}],
                ],
                dataLabels: {
                    enabled: true,
                    rotation: -90,
                    color: '#FFFFFF',
                    align: 'right',
                    format: '{point.y:f}', // one decimal
                    y: 10, // 10 pixels down from the top
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            }]
        });
    });
};