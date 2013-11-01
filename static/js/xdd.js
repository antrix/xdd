$(function() {

    if (!Modernizr.history) {
        return;
    }

    $( "a[data-pjax]" ).click(function(ev) {

        ev.preventDefault();
        fetchAphorism(this.href);

    });

    window.onpopstate = function(ev) {
        updatePageContent(ev.state);
    }

    var fetchInProgress = false;

    function fetchAphorism(url) {
        if (fetchInProgress) {
            return;
        }

        fetchInProgress = true;

        $.ajax({
            dataType: "json",
            cache: false,
            url: url + "index.json",
            complete: function() {
                fetchInProgress = false;
            },
            success: updatePageContent
        });
    }


});

function crossFadeText(locator, text) {
    $(locator).fadeOut(200, function() {
        $(this).text(text).fadeIn(200);
    });
}

function updatePageContent(aphorism) {
    if (typeof aphorism == "undefined" || aphorism == null || aphorism.slug.length == 0) {
        return;
    }

    if (window.location.pathname != aphorism.slug) {
        window.history.pushState(aphorism, null, aphorism.slug);
    }

    crossFadeText("#the-aphorism", aphorism.title);
    crossFadeText("#the-description", aphorism.desc);

    document.title = "[" + aphorism.title + "] driven development";

    $("#the-source").attr('href', aphorism.source);
    $("#the-permalink").attr('href', aphorism.slug);

    if (aphorism.prev_slug != null) {
        $("#the-prev").attr('href', aphorism.prev_slug);
        $("#the-prev").show();
    } else {
        $("#the-prev").hide();
    }

    if (aphorism.next_slug != null) {
        $("#the-next").attr('href', aphorism.next_slug);
        $("#the-next").show();
    } else {
        $("#the-next").hide();
    }
}
