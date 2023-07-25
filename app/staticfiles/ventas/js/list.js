var tblSale;
$(function () {
    tblSale = $('#data').DataTable({
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
            {"data": "Fecha"},
            {"data": "Hora"},
            {"data": "TpOperacion.Descripcion"},
            {"data": "IdDocumento.Descripcion"},
            {"data": "NroDocumento"},
            {"data": "Estado.Descripcion"},
            {"data": "Cliente.Nombre"},
            {"data": "Total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4, -5, -6, -7, -8, -9, -10],
                class: 'text-center',
                render: function (data, type, row) {
                    return data
                }
            },
            {
                targets: [-2],
                class: 'text-right',
                orderable: false,
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/ventas/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fa-solid fa-ban"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fa-regular fa-eye"></i></a> ';
                    buttons += '<a href="/erp/ventas/invoice/pdf/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fa-solid fa-print"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "Item"},
                    {"data": "Articulo.id"},
                    {"data": "Articulo.Descripcion"},
                    {"data": "Articulo.precio1"},
                    {"data": "Cant"},
                    {"data": "SubTotal"},
                    {"data": "Descuento"},
                    {"data": "Impuesto"},
                    {"data": "Total"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -2, -3, -4, -6],
                        class: 'text-right',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(3);
                        }
                    },
                    {
                        targets: [-5],
                        class: 'text-right',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-8, -9],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        });
});
