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
    

    //Show who has liked a post on hover of link
    $('.likers-link').mouseover(function(event) {
        event.preventDefault();
        linkID = this.id.slice(11);
        //alert('This is the link ID: '+ linkID);
        $('#likers-popup'+linkID).show();
    });

    //Hide who has liked a post when done hovering on link
    $('.likers-link').mouseout(function(event) {
        event.preventDefault();
        linkID = this.id.slice(11);
        //alert('This is the link ID: '+ linkID);
        $('#likers-popup'+linkID).hide();
    });

}