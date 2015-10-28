$(document).ready(function() {

    $('#like-btn').on("click", function(){
        event.preventDefault();
        alert('Hey');
        // var post_url = "/edit/profile";
        // var data = { 
        //     about_me: $("textarea#about_me").val(),
        //     job_title: $("input#job_title").val(),
        //     company: $("input#company").val(),
        //     linkedin: $("input#linkedin").val()
        // };
        if (false) {
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








