var tblProducts;
var vents = {
    items: {
        Fecha: '',
        IdDocumento: '',
        Caja: '',
        Moneda: '',
        Deposito: '',
        EmpresaEnvio: '',
        TpOperacion: '',
        Cliente: '',
        TpPago: '',
        Comentario: '',
        SubTotal: 0.00,
        Descuento: 0.00,
        Impuesto: 0.00,
        Total: 0.00,
        products: []
    },
    calculate_invoice: function() {
        var TSubTotal = 0.000;
        var TImpuesto = 0.000;
        var TTotal = 0.000;
        var TDescuentos = 0.000;
        $.each(this.items.products, function(pos, dict) {
            dict.SubTotal = parseFloat(dict.Cant) * (parseFloat(dict.PrecioVenta) - parseFloat(dict.Descuento));
            dict.Impuesto = dict.SubTotal * 0.18;
            dict.Total = dict.SubTotal + dict.Impuesto;
            TSubTotal+=dict.SubTotal;
            TImpuesto+=dict.Impuesto;
            TTotal+=dict.Total;
            TDescuentos+=dict.Descuento;
        });
        this.items.SubTotal = TSubTotal;
        this.items.Impuesto = TImpuesto;
        this.items.Total = TTotal;
        this.items.Descuento = TDescuentos;

        $('input[name="SubTotal"]').val(this.items.SubTotal.toFixed(2));
        $('input[name="Impuesto"]').val(this.items.Impuesto.toFixed(2));
        $('input[name="Total"]').val((parseFloat(this.items.SubTotal)+parseFloat(this.items.Impuesto)).toFixed(2));
        $('input[name="Descuento"]').val(this.items.Descuento.toFixed(2));
    },
    add: function(item){
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "Eli"},
                {"data": "id"},
                {"data": "Descripcion"},
                {"data": "PrecioVenta"},
                {"data": "Cant"},
                {"data": "SubTotal"},
                {"data": "Descuento"},
                {"data": "Impuesto"},
                {"data": "Total"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                 {
                    targets: [-8],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return data;
                    }
                },
                 {
                    targets: [-6],
                    class: 'text-right',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" style="direction: rtl;" step=".01" name="PrecioVenta" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.PrecioVenta+'">';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-right',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" style="direction: rtl;" step=".01" name="Cant" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.Cant+'">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-right',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" style="direction: rtl;" step=".01" name="DescuentoDet" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.Descuento+'">';
                    }
                },
                {
                    targets: [-4, -2, -1],
                    class: 'text-right',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="Cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 0.1,
                    decimals: 2,
                });
                $(row).find('input[name="DescuentoDet"]').TouchSpin({
                    min: 0,
                    max: 1000000000,
                    step: 0.1,
                    decimals: 2,
                });
                $(row).find('input[name="PrecioVenta"]').TouchSpin({
                    min: 0,
                    max: 1000000000,
                    step: 0.1,
                    decimals: 2,
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">'+
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.Imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Descripción:</b> ' + repo.Descripcion + '<br>' +
        '<b>Categoría:</b> ' + repo.Categoria.Descripcion + '<br>' +
        '<b>Precio Venta:</b> ' + repo.precio1 + '<br>' +
        '<b>Existencia:</b> ' + repo.Existencia +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#Fecha').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD"),
    });

    //$("input[name='Total']").TouchSpin({
    //    min: 0,
    //    max: 100,
    //    step: 0.1,
    //    decimals: 2,
    //    boostat: 5,
    //    maxboostedstep: 10,
    //    prefix : 'S/'
    //});
    // search products
/*
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            console.log(vents.items);
            vents.add(ui.item);
            $(this).val('');
        }
    });
*/
    $('#tblProducts tbody').on('change', 'input[name="PrecioVenta"]', function () {
        console.clear();
        var pvp = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].PrecioVenta = pvp;
        vents.calculate_invoice();
        $('td:eq(5)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].SubTotal.toFixed(2));
        $('td:eq(7)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].Impuesto.toFixed(2));
        $('td:eq(8)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].Total.toFixed(2));
    });

    $('#tblProducts tbody').on('change', 'input[name="Cant"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].Cant = cant;
        vents.calculate_invoice();
        $('td:eq(5)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].SubTotal.toFixed(2));
        $('td:eq(7)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].Impuesto.toFixed(2));
        $('td:eq(8)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].Total.toFixed(2));
    });

    $('#tblProducts tbody').on('change', 'input[name="DescuentoDet"]', function () {
        console.clear();
        var desct = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products[tr.row].Descuento = desct;
        vents.calculate_invoice();
        $('td:eq(5)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].SubTotal.toFixed(2));
        $('td:eq(7)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].Impuesto.toFixed(2));
        $('td:eq(8)', tblProducts.row(tr.row).node()).html(vents.items.products[tr.row].Total.toFixed(2));
        console.log(vents.items.products)
    });

    $('#tblProducts tbody').on('click', 'a[rel="remove"]', function () {
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.products.splice(tr.row, 1);
        vents.list();
    });

    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        vents.items.products = [];
        vents.list();
    });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        if(vents.items.products.length === 0){
            alert('xy');
            //message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }
        vents.items.Fecha = $('input[name="Fecha"]').val();
        vents.items.IdDocumento = $('select[name="IdDocumento"]').val();
        vents.items.Caja = $('select[name="Caja"]').val();
        vents.items.Moneda = $('select[name="Moneda"]').val();
        vents.items.Deposito = $('select[name="Deposito"]').val();
        vents.items.EmpresaEnvio = $('select[name="EmpresaEnvio"]').val();
        vents.items.TpOperacion = $('select[name="TpOperacion"]').val();
        vents.items.Cliente = $('select[name="Cliente"]').val();
        vents.items.TpPago = $('select[name="TpPago"]').val();
        vents.items.Comentario = $('input[name="Comentario"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: parameters,
                dataType: 'json',
                processData: false,
                contentType: false
            }).done(function (data) {
                console.log(data);
                if (!data.hasOwnProperty('error')) {
                    location.href = 'ret/';
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        return false;
    });

    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {results: data};
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

});
