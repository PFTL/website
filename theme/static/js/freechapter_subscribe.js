$(document).ready(function () {
  $('#free-chapter').submit(function (event) {
    event.preventDefault();

    var email = $("#email").val();
    $.ajax({
        type: "POST",
        url: "https://api.elasticemail.com/v2/contact/add",
        data: {
          'publicAccountID': '7616a022-4e37-40ba-b90e-6c3735d8440e',
          'email': email,
          'listName': 'Free PFTL Chapter',
          'activationTemplate': '',
          'source': 'WebForm',
          'ewf_captcha': 'false'},
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