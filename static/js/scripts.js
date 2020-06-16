
































/*$(document).ready(function(){


$('form').on('submit', function(event){
    let data = {
        name : $('#username').val(),
        paswword : $('#password').val()

    }

    $.ajax({
        data : JSON.stringify(data),
        dataType: "json",
        type: 'POST',
        url : 'login',
        contentType:"application/json; charset=UTF-8"
    })
    .done(function(data){
        console.log(data)
        if (data.error){
            $('#errorAlert').text(data.error).show;
        }
        else{
                console.log('It worked')
        }

    });

    event.preventDefault();

});

});
*/