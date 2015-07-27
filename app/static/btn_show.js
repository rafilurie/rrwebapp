window.onload = function() {

    $('#create-dropdown').hide();
    $('#help-dropdown').hide();
    
    document.getElementById("create-pdf").onclick = function() {
        $('#get-help').hide();
        $('#create-pdf').hide();
        $('#upload-btn').hide();
        $('#create-dropdown').show();    
    }

    $(".cancel").click(function(){
        $('#get-help').show();
        $('#create-pdf').show();
        $('#upload-btn').show();
        $('#create-dropdown').hide();
    });

    document.getElementById("get-help").onclick = function() {
        $('#get-help').hide();
        $('#create-pdf').hide();
        $('#upload-btn').hide();
        $('#help-dropdown').show();    
    }

    $(".cancel").click(function(){
        $('#get-help').show();
        $('#create-pdf').show();
        $('#upload-btn').show();
        $('#help-dropdown').hide();
    });



}