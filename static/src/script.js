setInterval(function(){
    // then fire off an ajax call
    RID = $('#uRID').val()
    console.log(RID)
    jQuery.ajax({
        url: '/chatlog/' + RID,
        success: function(response){
            // put some javascript here to do something with the
            // data that is returned with a successful ajax response,
            // as available in the 'response' param available,
            // inside this function, for example:
            $('#chatlog').html(response);
        },
    });
}, 1000);