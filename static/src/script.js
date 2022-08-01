refresh = function() {
    $('#chatlog').load('/',function(){
        refresh();
    });
}

$(function(){
    refresh();
});