document.addEventListener('DOMContentLoaded', function () {
    var ctxGeral = document.getElementById('myChart').getContext('2d');
    var myChartGeral = new Chart(ctxGeral, {
        type: 'bar',
        data: {
            labels: Object.keys(extratoData.meses),
            datasets: [{
                label: 'Diferença',
                data: Object.values(extratoData.meses).map(dados_mes => dados_mes.diferenca),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    // Gráfico de Pizza
    Object.entries(extratoData.meses).forEach(([mes, dados_mes]) => {
        generatePieChart(
            [dados_mes.total_receitas, dados_mes.total_despesas],
            ['Receitas', 'Despesas'],
            ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)'],
            ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
            `myPieChart_${mes}`
        );
    });
});

// Função para gerar gráfico de pizza
function generatePieChart(data, labels, backgroundColor, borderColor, chartId) {
    console.log('Data:', data);
    console.log('Labels:', labels);
    console.log('BackgroundColor:', backgroundColor);
    console.log('BorderColor:', borderColor);

    var ctx = document.getElementById(chartId).getContext('2d');
    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}
