$(document).ready(function () {

    $('form').on('submit', function (event) {

        $.ajax({
            data: {
                area: $('#area').val(),
                level: $('#level').val(),
                year: $('#year').val(),
                walls1: $('#walls_list_1').val(),
                walls2: $('#walls_list_2').val(),
                districts: $('#districts').val(),
                dist1: $('#dist1').val(),
                dist2: $('#dist2').val(),
                code: $('#code').val(),
                predict: $('#preidct').val()


            },
            type: 'POST',
            url: '/process'
        })
            .done(function (data) {

                if (data.error) {
                    alert(data.error)
                }
                else {
                    alert(data.predict)
                }

            });
        event.preventDefault();

    });

});