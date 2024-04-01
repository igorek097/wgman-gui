document.body.addEventListener('htmx:afterSwap', function (evt) {
    setTimeout(function() {
        var focus = document.querySelector('[autofocus]');
        if (focus) {
            focus.focus();
        }
    }, 500)
});


document.body.addEventListener('htmx:beforeSwap', function (event) {
    var url = new URL(event.detail.xhr.responseURL)
    if (url.pathname == event.detail.xhr.url) {
        return
    }
    event.detail.shouldSwap = false;
    window.location.href = url;
});