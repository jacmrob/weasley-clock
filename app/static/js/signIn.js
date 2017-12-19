$(function() {
    $('#btnSignIn').click(function() {
 
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function (response) {
                window.location.href = '/dashboard';
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});