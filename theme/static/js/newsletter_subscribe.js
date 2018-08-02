$(document).ready(function () {
  $('#newsletter').submit(function (event) {
    event.preventDefault();

    var email = $("#email").val();
    $.ajax({
        type: "POST",
        url: "https://api.elasticemail.com/v2/contact/add",
        data: {
          'publicAccountID': '7616a022-4e37-40ba-b90e-6c3735d8440e',
          'email': email,
          'listName': 'PFTL Newsletter',
          'activationTemplate': 'New_Account_Confirmation',
          'source': 'WebForm',
          'ewf_captcha': 'false'},
        beforeSend: function () {
          $("#send").prop("disabled", true);
          $("#send").text("Sending");
        },
        success: function (data) {
          $("#newsletter_feedback").html('<div class="alert alert-primary" role="alert">Thanks for signing up to our newsletter!</div>');
        },
        error: function () {
          $("#newsletter_feedback").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
          $("#send").prop("disabled", false);
        }
       });
  });
  $('#newsletter-sidebar').submit(function (event) {
    event.preventDefault();

    var email = $("#email-sidebar").val();
    $.ajax({
        type: "POST",
        url: "https://api.elasticemail.com/v2/contact/add",
        data: {
          'publicAccountID': '7616a022-4e37-40ba-b90e-6c3735d8440e',
          'email': email,
          'listName': 'PFTL Newsletter',
          'activationTemplate': 'New_Account_Confirmation',
          'source': 'WebForm',
          'ewf_captcha': 'false'},
        beforeSend: function () {
          $("#send-sidebar").prop("disabled", true);
          $("#send-sidebar").text("Sending");
        },
        success: function (data) {
          $("#newsletter_feedback-sidebar").html('<div class="alert alert-primary" role="alert">Thanks for signing up to our newsletter!</div>');
        },
        error: function () {
          $("#newsletter_feedback-sidebar").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
          $("#send-sidebar").prop("disabled", false);
        }
       });
  });
  $('#newsletter-popup').submit(function (event) {
    event.preventDefault();

    var email = $("#email-popup").val();
    $.ajax({
        type: "POST",
        url: "https://api.elasticemail.com/v2/contact/add",
        data: {
          'publicAccountID': '7616a022-4e37-40ba-b90e-6c3735d8440e',
          'email': email,
          'listName': 'PFTL Newsletter',
          'activationTemplate': 'New_Account_Confirmation',
          'source': 'WebForm',
          'ewf_captcha': 'false'},
        beforeSend: function () {
          $("#send-popup").prop("disabled", true);
          $("#send-popup").text("Sending");
        },
        success: function (data) {
          $("#newsletter_feedback-popup").html('<div class="alert alert-primary" role="alert">Thanks for signing up to our newsletter!</div>');
        },
        error: function () {
          $("#newsletter_feedback-popup").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
          $("#send-popup").prop("disabled", false);
        }
       });
  });
});