$(document).ready(function() {

    $("#gridContainer").dxDataGrid({
        dataSource: data,
        showBorders: true,
        showRowLines: true,
        columnAutoWidth: true,
        remoteOperations: true,
        hoverStateEnabled: true,        
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
        headerFilter: {
            visible: true,
            height: 500,
            width: 400
        },
        loadPanel: {
            enabled: true
        },
    });
});