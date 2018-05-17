$(document).ready(function () {
    $.ajax({
        dataType: "html",
        url: '/latest_articles.html',
        success: function(data) {
            $("#latest_articles").fadeOut(function () {
                $(this).html(data).slideDown();
            });
        }
    });
});