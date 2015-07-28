// // Hide edit form when the user comes to the profile page

$(document).ready(function() {

    $('#aboutme-form').hide();

    $('#about-me-container').on("click", ".aboutme-action", function(event) {
        event.preventDefault();
        $('#aboutme-form').show();
        $('.aboutme-action').hide();
        $('#about-me-text').hide();
    });

    $('#aboutme-form').on("click", "#edit-cancel-btn", function(event) {
        event.preventDefault();
        $('#aboutme-form').hide();
        $('.aboutme-action').show();
        $('#about-me-text').show();
    });

    $("#aboutme-form").submit(function(event) {
        event.preventDefault();
        var post_url = "/edit/aboutme";
        var data = { content: $("textarea#about_me").val() }

        if ($("textarea#about_me").val() != "") {
            $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                url: post_url,
                data: JSON.stringify({content: $("textarea#about_me").val() }),
                success: function(data) {
                    update_aboutme(data.contents);
                },
                dataType: "json"
            });
        }
    });
});

var update_aboutme = function(content) {
    $('#add-aboutme').hide();
    $('#aboutme-form').hide();
    var new_html = "";
    new_html += "<p id='about-me-text'>";
    new_html += content;
    new_html += "</p>";
    new_html += "<a class='aboutme-action' id='edit-aboutme'>Edit About Me</a>";
    $("#about-me-container").html(new_html);
    $('#about-me-container').on("click", ".aboutme-action", function(event) {
        event.preventDefault();
        $('#aboutme-form').show();
        $('.aboutme-action').hide();
    });
    $('#about-me-text').show();

}








