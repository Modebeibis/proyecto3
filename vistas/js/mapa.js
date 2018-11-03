var states = ['AGU', 'BCN', 'BCS', 'CAM', 'CHH',
                'CHP', 'COA', 'COL', 'DIF', 'DUR',
                'GRO', 'GUA', 'HID', 'JAL', 'MEX',
                'MIC', 'MOR', 'NAY', 'NLE', 'OAX',
                'PUE', 'QUE', 'ROO', 'SIN', 'SLP',
                'SON', 'TAB', 'TAM', 'TLA', 'VER',
                'YUC', 'ZAC'];

        var state_names = ['Aguascalientes', 'Baja California Norte',
        'Baja California Sur', 'Campeche', 'Chihuahua', 'Chiapas', 'Coahuila',
        'Colima', 'Ciudad de México', 'Durango', 'Guerrero', 'Guanajuato',
        'Hidalgo', 'Jalisco', 'Edo. Mexico', 'Michoacán', 'Morelos', 'Nayarit',
        'Nuevo León', 'Oaxaca', 'Puebla', 'Queretaro', 'Quintana Roo', 'Sinaloa',
        'San Luis Potosí', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala',
        'Veracruz', 'Yucatán', 'Zacatecas'];

        $(function () {
            $('.map').maphilight({ fade: false });
        });
        $(document).ready(function () {
            $('.area').hover(function () {
                var id = $(this).attr('id');
                var state = $.inArray(id, states);

                $('#edo').html(state_names[state]);
            });
        });