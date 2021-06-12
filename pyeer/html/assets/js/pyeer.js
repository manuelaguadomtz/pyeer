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
});