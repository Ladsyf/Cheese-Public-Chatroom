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

    $("#searchQuery").keyup(function(){
        query = $("#searchQuery").val()
        if (query == ""){
            query = ""
        }
        $.ajax({
            method: "GET",
            url: '/',
            data: "query="+query
        }).done(function(data){
            $("#roomsList").html(data)
        });
    });


});
function sendMessageAfter(){
    RID = $('#uRID').val()
    Message = $('#message').val()
    $('#message').val('').focus()
        antiSpam()
}

function send(RID, Message){
    if (Message == ""){
        return
    }
         $.ajax({
         method: "POST",
         url: '/addMsg',
         data: "RID=" + RID + "&message=" + Message
    }).done(function(response){
        $('#chatlog').html(response);
        console.log("test")
    });
}

function flushflash(){
    $('.flushflash').hide();
}
function antiSpam(){
    messageCountSeconds = 5

    $("#message").attr("placeholder", "You can send a message again in " + messageCountSeconds)
    $("#send").prop("disabled", true)
    $("#message").prop("disabled", true)
    start = setInterval(function () {
    messageCountSeconds = messageCountSeconds - 1
    $("#message").attr("placeholder", "You can send a message again in " + messageCountSeconds)
        if(messageCountSeconds <= 0){
            stopCounting(start)
        }
    },1000);

}
function stopCounting(timer){
      $("#message").prop("disabled", false)
      $("#send").prop("disabled", false)
      $("#message").attr("placeholder", "Enter your anonymous message here...")
      clearInterval(timer)
}