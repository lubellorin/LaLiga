$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "Imagen"},
            {"data": "Descripcion"},
            {"data": "CodigoBarra"},
            {"data": "Categoria.Descripcion"},
            {"data": "Modelo"},
            {"data": "precioCompra"},
            {"data": "precio1"},
            {"data": "Existencia"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-10],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [-9],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [-4],
                class: 'text-right',
                orderable: false,
                render: function (data, type, row) {
                    return 'S/ '+parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-3],
                class: 'text-right',
                orderable: false,
                render: function (data, type, row) {
                    return 'S/ '+parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2],
                class: 'text-right',
                orderable: false,
                render: function (data, type, row) {
                    if(row.Existencia > 0){
                        return '<span class="badge badge-success">'+data+'</span>'
                    }
                    return '<span class="badge badge-danger">'+data+'</span>'
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/product/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/product/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
