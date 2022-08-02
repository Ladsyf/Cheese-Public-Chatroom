//setInterval(function(){
//    // then fire off an ajax call
//    RID = $('#uRID').val()
//    console.log(RID)
//    jQuery.ajax({
//        url: '/chatlog/' + RID,
//        success: function(response){
//            // put some javascript here to do something with the
//            // data that is returned with a successful ajax response,
//            // as available in the 'response' param available,
//            // inside this function, for example:
//            $('#chatlog').html(response);
//        },
//    });
//}, 1000);

//function poll() {
//        var poll_interval=100
//        RID = $('#uRID').val()
//        console.log(RID)
//        jQuery.ajax({
//                url: '/chatlog/' + RID,
//                type: 'GET',
//                success: function(data) {
//                        $('#chatlog').html(data)
//                        poll_interval=100;
//                },
//                error: function () {
//                        poll_interval=1000;
//                },
//                complete: function () {
//                        setTimeout(poll, poll_interval);
//                },
//        });
//}
//poll()
$(document).ready(function(){
    RID = $('#uRID').val()
    $('#send').click(function(){
    Message = $('#message').val()
        send(RID, Message)
    })
});
function send(RID, Message){
    console.log(RID + " " + Message)
         $.ajax({
         method: "POST",
         url: '/addMsg',
         data: "RID=" + RID + "&message=" + Message
    }).done(function(response){
        $('#chatlog').html(response);
    });
}