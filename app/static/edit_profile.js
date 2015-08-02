// // Hide edit form when the user comes to the profile page

$(document).ready(function() {

    $('#edit-profile-form').on("click","#save-btn", function(){
        event.preventDefault();
        var post_url = "/edit/profile";
        var data = { 
            about_me: $("textarea#about_me").val(),
            job_title: $("input#job_title").val(),
            company: $("input#company").val(),
            linkedin: $("input#linkedin").val()
        };
        if ($("textarea#about_me").val() != "" || $("input#job_title").val() != "" || $("input#company").val() != "" || $("input#linkedin").val() != "") {
            $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                url: post_url,
                data: JSON.stringify(
                    {about_me: $("textarea#about_me").val(),
                    job_title: $("input#job_title").val(),
                    company: $("input#company").val(),
                    linkedin: $("input#linkedin").val()
                    }
                ),
                success: function(data) {
                    update_aboutme(data.about_me, data.job_title, data.company, data.linkedin);
                },
                dataType: "json"
            });
        }
    });
});

var update_aboutme = function(about_me, job_title, company, linkedin) {
    if (about_me != "") {
        var new_html = "";
        new_html += "<div id='about_me-text'>";
        new_html += about_me;
        new_html += "</div>";
        $("#about_me-text").html(new_html);
    }
    if (job_title != "") {
        var new_html = "";
        new_html += "<div id='job_title-text'>";
        new_html += job_title;
        new_html += "</div>";
        $("#job_title-text").html(new_html);
    }
    if (company != "") {
        var new_html = "";
        new_html += "<div id='company-text'>";
        new_html += company;
        new_html += "</div>";
        $("#company-text").html(new_html);
    }
    if (linkedin != "") {
        var new_html = "";
        new_html += "<div id='linkedin-text'>";
        new_html += linkedin;
        new_html += "</div>";
        $("#linkedin-text").html(new_html);
    }
    // $('#edit-profile-modal').modal('toggle');
    $('div.modal-content').hide();
    window.location.reload();

}








