$(document).ready(function() {

    $('form').on('submit', function(event){

        $.ajax({

            data : {
                name : $('#username').val(),
                password : $('#password').val()

            },
            type: 'POST',
            url : '/login'
        })
        .done(function(data){
          if (data.error) {
                $('#errorAlert').text(data.error).show();
          }
          else {
                console.log('It worked')
          }

        });
        
        event.preventDefault();

    });

});