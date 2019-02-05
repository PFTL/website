from docutils.parsers.rst import directives, Directive
from docutils import nodes


newsletter_div = """
<div class="card border-primary mb-3">
    <div class="card-header">Subscribe</div>
    <div class="card-body">
        <h4 class="card-title">Get all the information directly to your inbox</h4>
        <div id="newsletter_feedback-inline"></div>
        <form id="newsletter-inline">
            <div class="form-group">
                <input class="form-control" type="email" id="email-inline" placeholder="Your E-mail" required>
            </div>
            <div class="form-group">
                <input class="btn btn-danger col-sm-12" type="submit"
                       value="Subscribe to the newsletter" id="send-inline">
            </div>
        </form>
        <p class="card-text">Get relevant information, unsubscribe at any time.</p>
    </div>
</div>
"""


class Newsletter(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = False

    def run(self):
        return [nodes.raw('', newsletter_div, format='html'),]


def register():
    directives.register_directive('newsletter', Newsletter)
