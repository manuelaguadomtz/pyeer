$(document).ready(function() {

    $("#gridContainerGeneral").dxDataGrid({
        dataSource: data,
        showBorders: true,
        showRowLines: true,
        columnAutoWidth: true,
        showColumnLines: true,
        allowColumnReordering: true,
        allowColumnResizing: true, 
        columnResizingMode: "nextColumn",
        columnChooser: {
            enabled: true,
            mode: "select" // or "dragAndDrop"
        },
        filterRow: {
            visible: true,
            applyFilter: "auto"
        },
        export: {
            enabled: true,
        },
        headerFilter: {
            visible: true,
            height: 500,
            width: 400
        },
        loadPanel: {
            enabled: true
        },
        columns: [
            {
                dataField: "experiment",
                caption: "Experiment",
                allowHiding: false,
                allowReordering: false,
                fixed: true,
            },
            {
                dataField: "gmean",
                caption: "Genuine scores mean",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,

            },
            {
                dataField: "gstd",
                caption: "Genuine scores STD",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "imean",
                caption: "Impostor scores mean",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "istd",
                caption: "Impostor scores STD",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "sindex",
                caption: "Sensitivity index (d')",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "jndex",
                caption: "Youden's Index",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "MCC",
                caption: "Matthews Correlation Coefficient",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
        ],
        onExporting: function(e) {
            var workbook = new ExcelJS.Workbook();
            var worksheet = workbook.addWorksheet('General Stats');
          
            DevExpress.excelExporter.exportDataGrid({
                component: e.component,
                worksheet: worksheet,
                autoFilterEnabled: true
            }).then(function() {
                workbook.xlsx.writeBuffer().then(function(buffer) {
                    saveAs(new Blob([buffer], { type: 'application/octet-stream' }), 'General Stats.xlsx');
                });
            });
            e.cancel = true;
        },
    });

    $("#gridContainerErrors").dxDataGrid({
        dataSource: data,
        showBorders: true,
        showRowLines: true,
        columnAutoWidth: true,
        showColumnLines: true,
        allowColumnReordering: true,
        allowColumnResizing: true, 
        columnResizingMode: "nextColumn",
        export: {
            enabled: true,
        },
        columnChooser: {
            enabled: true,
            mode: "select" // or "dragAndDrop"
        },
        filterRow: {
            visible: true,
            applyFilter: "auto"
        },
        headerFilter: {
            visible: true,
            height: 500,
            width: 400
        },
        loadPanel: {
            enabled: true
        },
        columns: [
            {
                dataField: "experiment",
                caption: "Experiment",
                allowHiding: false,
                allowReordering: false,
                fixed: true,
            },
            {
                dataField: "EERLow",
                caption: "EER Low",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,

            },
            {
                dataField: "EERHigh",
                caption: "EER High",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "EER",
                caption: "EER",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "ZeroFMR",
                caption: "ZeroFMR",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR1000",
                caption: "FMR1000",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR100",
                caption: "FMR100",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR20",
                caption: "FMR20",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR10",
                caption: "FMR10",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "ZeroFNMR",
                caption: "ZeroFNMR",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "AUC",
                caption: "AUC",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
        ],
        onExporting: function(e) {
            var workbook = new ExcelJS.Workbook();
            var worksheet = workbook.addWorksheet('Errors');
          
            DevExpress.excelExporter.exportDataGrid({
                component: e.component,
                worksheet: worksheet,
                autoFilterEnabled: true
            }).then(function() {
                workbook.xlsx.writeBuffer().then(function(buffer) {
                    saveAs(new Blob([buffer], { type: 'application/octet-stream' }), 'Errors.xlsx');
                });
            });
            e.cancel = true;
        },
    });

    $("#gridContainerThresholds").dxDataGrid({
        dataSource: data,
        showBorders: true,
        showRowLines: true,
        columnAutoWidth: true,
        showColumnLines: true,
        allowColumnReordering: true,
        allowColumnResizing: true, 
        columnResizingMode: "nextColumn",
        columnChooser: {
            enabled: true,
            mode: "select" // or "dragAndDrop"
        },
        export: {
            enabled: true,
        },
        filterRow: {
            visible: true,
            applyFilter: "auto"
        },
        headerFilter: {
            visible: true,
            height: 500,
            width: 400
        },
        loadPanel: {
            enabled: true
        },
        columns: [
            {
                dataField: "experiment",
                caption: "Experiment",
                allowHiding: false,
                allowReordering: false,
                fixed: true,
            },
            {
                dataField: "EERTh",
                caption: "EER",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,

            },
            {
                dataField: "ZeroFMRTh",
                caption: "ZeroFMR",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR1000Th",
                caption: "FMR1000",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR100Th",
                caption: "FMR100",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR20Th",
                caption: "FMR20",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "FMR10Th",
                caption: "FMR10",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "ZeroFNMRTh",
                caption: "ZeroFNMR",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "jindexTh",
                caption: "Youden's Index",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
            {
                dataField: "MCCTh",
                caption: "Matthews Correlation Coefficient",
                allowHiding: true,
                allowReordering: true,
                allowHeaderFiltering: false,
            },
        ],
        onExporting: function(e) {
            var workbook = new ExcelJS.Workbook();
            var worksheet = workbook.addWorksheet('Errors');
          
            DevExpress.excelExporter.exportDataGrid({
                component: e.component,
                worksheet: worksheet,
                autoFilterEnabled: true
            }).then(function() {
                workbook.xlsx.writeBuffer().then(function(buffer) {
                    saveAs(new Blob([buffer], { type: 'application/octet-stream' }), 'Tresholds.xlsx');
                });
            });
            e.cancel = true;
        },
    });

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