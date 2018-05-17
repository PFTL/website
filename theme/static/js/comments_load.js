$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/comments/{{ article.url }}comments.html',
        success: function (data) {
            $('#current-comments').html(data);
        },
        error: function () {
            $('#current-comments').html('<h3 class="mb-3">No comments yet, be the first!</h3>');
        }
    });
});