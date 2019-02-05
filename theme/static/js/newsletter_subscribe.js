$(document).ready(function () {
  $('#newsletter').submit(function (event) {
    event.preventDefault();

    var email = {'email': $("#email").val()};
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        url: "https://uetke.uetke.com/subscribe-newsletter",
        data: JSON.stringify(email),
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

    var email = {'email': $("#email-sidebar").val()};
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        url: "https://uetke.uetke.com/subscribe-newsletter",
        data: JSON.stringify(email),
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
  $('#newsletter-inline').submit(function (event) {
        event.preventDefault();
    var email = {'email': $("#email-inline").val()};
    $.ajax({
        type: "POST",
        dataType: 'json',
        contentType: 'application/json',
        url: "https://uetke.uetke.com/subscribe-newsletter",
        data: JSON.stringify(email),
        beforeSend: function () {
          $("#send-inline").prop("disabled", true);
          $("#send-inline").text("Sending");
        },
        success: function (data) {
          $("#newsletter_feedback-inline").html('<div class="alert alert-primary" role="alert">Thanks for signing up to our newsletter!</div>');
        },
        error: function () {
          $("#newsletter_feedback-inline").html('<div class="alert alert-danger" role="alert">An error ocurred, please try again!</div>');
          $("#send-inline").prop("disabled", false);
        }
       });
  });
});