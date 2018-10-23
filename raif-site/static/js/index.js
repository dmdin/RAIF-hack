$(document).ready(function () {

    $('form').on('submit', function (event) {

        $.ajax({
            data: {
                area: $('#area').val(),
                level: $('#level').val(),
                year: $('#year').val(),
                walls1: $('#walls_list_1').val(),
                walls2: $('#walls_list_2').val(),
                districts: $('#districts').val()


            },
            type: 'POST',
            url: '/process'
        })
            .done(function (data) {

                if (data.error) {
                    alert('Коля пидарас поля не заполнил')
                }
                else {
                    alert('Area: ' + data.area + ' Level: ' + data.level + ' Дохуя стоит!')
                }

            });
        event.preventDefault();

    });

});