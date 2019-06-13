window.FunnelTools || (window.FunnelTools = {});
FunnelTools.Capture = {
    showTime: 32000,

    init: function (opts) {
        if (opts && opts.showTime) {
            this.showTime = opts.showTime;
        }
        this.widget().css('bottom', '-' + this.position() + "px");
        this.triggerShow(this.showTime);
    },
    widget: function () {
        return $("#funnel-tools-capture");
    },
    open: function () {
        return $("#funnel-tools-capture .open");
    },

    close: function () {
        return $("#funnel-tools-capture .close");
    },
    show: function () {
        this.widget().animate({bottom: 0}, 200);
        this.widget().addClass('open');
    },
    triggerShow: function (time) {
        var that = this;

        setTimeout(function () {
                that.show();
        }, time);
    },
    hide: function () {
        this.widget().animate({bottom: '-' + this.position() + 'px'}, 200);
        this.widget().removeClass('open');
    },
    toggle: function () {
        if (!this.isVisible()) {
            this.show();
        } else {
            this.hide();
        }
    },
    isVisible: function () {
        return this.widget().hasClass('open');
    },
    position: function () {
        return this.height() - this.titleHeight();
    },
    height: function () {
        return this.widget()[0].scrollHeight;
    },
    titleHeight: function () {
        if (this.widget().css('border-radius') === "0px") {
            return 30;
        } else {
            return 45;
        }
    }
};

$(document).on("click", "#funnel-tools-capture .title, #funnel-tools-capture .open, #funnel-tools-capture .close", function () {
    FunnelTools.Capture.toggle();
});

// Hide widget when clicking outside
$(document).click(function (event) {
    if (!FunnelTools.Capture.isVisible()) {
        return;
    }
    if ($(event.target).parents("#funnel-tools-capture").length === 0) {
        FunnelTools.Capture.hide();
    }
});



$(document).ready(function () {
    FunnelTools.Capture.init();
    $("#funnel-tools-capture form").submit(function (event) {
        var $form = $(event.target);
        var $submit = $form.find('*[type=submit]');
        var $title = $("#funnel-tools-capture .title");
        var $description = $("#funnel-tools-capture .description");
        var $email = $("#funnel-tools-capture input[type=email]");
        $submit
            .prop('disabled', true)
            .data('submitText', $submit.text())
            .text('Subscribing...');

        $.ajax({
            url: $form.attr('action'),
            method: 'POST',
            data: JSON.stringify(email),
        }).always(function () {
            $submit
                .prop('disabled', false)
                .text($submit.data('submitText'));
        }).done(function (data, textStatus, xhr) {
            if (xhr.status === 201) {
                $title.html('Thanks for signing up!');
                $description.html('Please check your email to confirm your subscription.');
            } else {
                alert("An unexpected error occurred while submitting this form, we are sorry!");
                console.error(data.reason);
            }
        }).fail(function (xhr, textStatus, error) {
            if (xhr.status === 401) {
                $description.html("You've already signed up with that email.")
            } else if (xhr.status === 400) {
                $email.next('span.error').remove();
                $email.after('<span class="error">Invalid Email</span>');
                $email.addClass('error');
            } else {
                alert("An unexpected error occurred while submitting this form, we are sorry!");
            }
        });
        event.preventDefault();
    });
    $("#funnel-tools-capture input[type=email]").focus(function (event) {
        var $email = $(event.target);
        $email.removeClass('error');
        $email.next('span.error').remove();
    });
});
