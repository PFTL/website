(function(window,d){
    if (!window) return;
    var browser = window.navigator;
    var url_info = window.location;
    var document = window.document;
    var user_agent = browser.userAgent;
    var last_url;

    var post = function(options) {
      var isPushState = options && options.isPushState;

      // Standardize url information
      var url = url_info.protocol + '//' + url_info.hostname + url_info.pathname;

      // Don't send the last URL again (this could happen when pushState is used to change the URL hash or search)
      if (lastSendUrl === url) return;
      lastSendUrl = url;

      // ignore prerendered pages
    if( 'visibilityState' in document && document.visibilityState === 'prerender' ) {
      return;
    }

    // if <body> did not load yet, try again at dom ready event
    if( document.body === null ) {
      document.addEventListener("DOMContentLoaded", () => {
        trackPageview(vars);
      })
      return;
    }

    // do not track if not served over HTTP or HTTPS (eg from local filesystem)
    if(url_info.host === '') {
      return;
    }
    var data = {url: url };
    if (user_agent) data.ua = user_agent;
    if (document.referrer && !isPushState) data.referrer = document.referrer;
    if (window.innerWidth) data.width = window.innerWidth;
    if (window.innerHeight) data.height = window.innerHeight;
    console.log(JSON.stringify(data));
    var request = new XMLHttpRequest();
    request.open('POST', d + '/post', true);
    request.setRequestHeader('Content-Type', 'text/plain; charset=UTF-8');
    request.send(JSON.stringify(data));
    }

    // Thanks to https://gist.github.com/rudiedirkx/fd568b08d7bffd6bd372
    var his = window.history;
    if (his && his.pushState && Event && window.dispatchEvent) {
      var stateListener = function(type) {
        var orig = his[type];
        return function() {
          var rv = orig.apply(this, arguments);
          var event = new Event(type);
          event.arguments = arguments;
          window.dispatchEvent(event);
          return rv;
        };
      };
      his.pushState = stateListener('pushState');
      window.addEventListener('pushState', function() {
        post({ isPushState: true });
      });
    }
    post();
})(window, 'https://www.privalytics.io/api/tracker');