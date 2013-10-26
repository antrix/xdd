$(function() {

    if (!Modernizr.history) {
        return;
    }

    $( "#the-aphorism" ).click(function(ev) {

        ev.preventDefault();

        var ap = Aphorisms.pop();

        updatePageContent(ap);

        fetchMoreIfNeeded();
    });

    window.onpopstate = function(ev) {
        updatePageContent(ev.state);
    }

    var fetchInProgress = false;

    function fetchMoreIfNeeded() {
        if (fetchInProgress || Aphorisms.length > 2) {
            return;
        }

        fetchInProgress = true;

        $.ajax({
            dataType: "json",
            cache: false,
            url: "/a/random",
            complete: function() {
                fetchInProgress = false;
            },
            success: function(data) {
                if (data.Aphorisms.length > 0) {
                    Aphorisms = data.Aphorisms.concat(Aphorisms);
                }
            }
        });
    }


});

function crossFadeText(locator, text) {
    $(locator).fadeOut(200, function() {
        $(this).text(text).fadeIn(200);
    });
}

function updatePageContent(aphorism) {
    if (typeof aphorism == "undefined" || aphorism == null || aphorism.permalink.length == 0) {
        return;
    }

    if (window.location.pathname != aphorism.permalink) {
        window.history.pushState(aphorism, null, aphorism.permalink);
    }

    crossFadeText("#the-aphorism", aphorism.x);
    crossFadeText("#the-description", aphorism.desc);

    document.title = "[" + aphorism.x + "] driven development";

    $("#the-source").attr('href', aphorism.source);
    $("#the-permalink").attr('href', aphorism.permalink);
}
