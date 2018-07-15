$(document).ready(function () {
  $('#comment-form').submit(function (event) {
    event.preventDefault();
    data = $('#comment-form').serialize();
    $.ajax({
        type: "POST",
        url: "https://api.staticman.net/v2/entry/PFTL/website_comments/master/comments",
        data: data,
        beforeSend: function () {
          $("#submit").prop("disabled", true);
          $("#submit").html('<img src="/theme/img/Pacman_Spinner.svg" style="height: 20px;">');
          $("#id").prop("disabled", true);
        },
        success: function (data) {
            console.log('Success');
          $(".comment").html('<div class="alert alert-primary" role="alert">Thanks for your comment. It will appear here as soon as it gets approved!</div>');
        },
        error: function () {
          $("#newsletter_feedback").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
        }
       });
  });
});