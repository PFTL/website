$(document).ready(function () {
  $('#free-chapter').submit(function (event) {
    event.preventDefault();

    var email = {'email': $("#email").val()};
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        url: "https://uetke.uetke.com/free-chapter",
        data: JSON.stringify(email),
        beforeSend: function () {
          $("#send").prop("disabled", true);
          $("#send").text("Sending");
        },
        success: function (data) {
          $("#newsletter_feedback").html('<div class="alert alert-primary" role="alert">Thanks for signing up to our newsletter!</div>');
        },
        error: function (data) {
          $("#newsletter_feedback").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
        }
       });
  });
});