window.onload = function() {

    // $('#create-dropdown').hide();
    // $('#help-dropdown').hide();

    $('.delete-btn').on("click", function(event) {
        event.preventDefault();
        var post_url = "/delete";
        var deletelinkID = $(this).attr('id');
        var linkID = deletelinkID.slice(6);
        //alert(deletelinkID);
        //alert(linkID);
        //var data = { content: $("textarea#about_me").val() }

        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: post_url,
            data: (linkID),
            success: function(response) {
                $('#article'+linkID).remove();
            },
            dataType: "json"
        });
    });

}