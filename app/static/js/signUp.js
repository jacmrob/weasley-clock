$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/register',
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