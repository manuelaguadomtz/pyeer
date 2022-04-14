$(document).ready(function() {

    /* Charts */
    const colors = [
        'rgb(219, 2, 2)',
        'rgb(20, 5, 237)',
        'rgb(35, 219, 2)',
        'rgb(237, 229, 5)',
        'rgb(5, 222, 237)',
        'rgb(237, 5, 214)',
        'rgb(237, 5, 140)',
        'rgb(242, 82, 82)',
        'rgb(10, 3, 3)',
        'rgb(242, 165, 82)',
        'rgb(242, 210, 82)',
        'rgb(191, 242, 82)',
        'rgb(82, 242, 181)',
        'rgb(82, 162, 242)',
        'rgb(152, 102, 232)',
        'rgb(102, 113, 232)',
        'rgb(232, 102, 215)',
        'rgb(232, 102, 141)',
    ]

    /* DET curve */
    var detDatasets = [];
    var i;
    for(i = 0; i < data.length; i++)
    {
        var dSet = {
            label: data[i].experiment,
            data: data[i].fnmr_samples,
            backgroundColor: colors[i % colors.length],
            borderColor: colors[i % colors.length],
            fill: false,
        }
        detDatasets.push(dSet);
    }

    const detConfig = {
        type: 'line',
        data: {
            labels: data[0].samples,
            datasets: detDatasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'False match rate'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'False non-match rate'
                    },
                }
            }
        }
    };

    var ctx = document.getElementById('detChart').getContext('2d');
    window.detChart = new Chart(ctx, detConfig);

    /* DET Log curve */

    const detLogConfig = {
        type: 'line',
        data: {
            labels: data[0].samples,
            datasets: detDatasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
            scales: {
                x: {
                    display: true,
                    type: 'logarithmic',
                    title: {
                        display: true,
                        text: 'False match rate'
                    }
                },
                y: {
                    display: true,
                    type: 'logarithmic',
                    title: {
                        display: true,
                        text: 'False non-match rate'
                    },
                }
            }
        },
    };

    var ctx = document.getElementById('detChartLog').getContext('2d');
    window.detChartLog = new Chart(ctx, detLogConfig);

    /* ROC curve */
    var rocDatasets = [];
    var i;
    for(i = 0; i < data.length; i++)
    {
        var dSet = {
            label: data[i].experiment,
            data: data[i].tpr_samples,
            backgroundColor: colors[i % colors.length],
            borderColor: colors[i % colors.length],
            fill: false,
        }
        rocDatasets.push(dSet);
    }

    const rocConfig = {
        type: 'line',
        data: {
            labels: data[0].samples,
            datasets: rocDatasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'False match rate'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'True match rate'
                    },
                }
            }
        },
    };

    var ctx = document.getElementById('rocChart').getContext('2d');
    window.rocChart = new Chart(ctx, rocConfig);

    /* ROC Log curve */
    const rocLogConfig = {
        type: 'line',
        data: {
            labels: data[0].samples,
            datasets: rocDatasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
            scales: {
                x: {
                    display: true,
                    type: 'logarithmic',
                    title: {
                        display: true,
                        text: 'False match rate'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'True match rate'
                    },
                }
            }
        },
    };

    var ctx = document.getElementById('rocChartLog').getContext('2d');
    window.rocChartLog = new Chart(ctx, rocLogConfig);

});