$(function() {

    if (!Modernizr.history) {
        return;
    }

    $( "a[data-pjax]" ).click(function(ev) {

        ev.preventDefault();
        fetchAphorism(this.href);

    });

    $("#the-tweet").click(onTweetClick);

    window.onpopstate = function(ev) {
        updatePageContent(ev.state);
    }

    var fetchInProgress = false;

    function fetchAphorism(url) {
        if (fetchInProgress) {
            return;
        }

        fetchInProgress = true;

        $("body").css("cursor", "progress");

        $.ajax({
            dataType: "json",
            cache: true,
            url: url + "index.json",
            complete: function() {
                fetchInProgress = false;
                $("body").css("cursor", "default");
            },
            success: updatePageContent
        });
    }


});

function crossFadeText(locator, text) {
    $(locator).fadeOut(200, function() {
        $(this).html(text).fadeIn(200);
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

    document.title = "What is " + aphorism.title + " driven development?";

    var meta=document.getElementsByTagName("meta");
    for (var i=0; i<meta.length; i++) {
        if (meta[i].name.toLowerCase() == "description") {
            meta[i].content = aphorism.title + " driven development: a tongue-in-cheek definition drawn from the wisdom of software practitioners"
        }
    }

    if (aphorism.source != null) {
        $("#the-source").attr('href', aphorism.source);
        $("#the-source").html('<i class="fa fa-external-link-square"></i>');
    } else {
        $("#the-source").attr('href', 'mailto:dev@devdriven.by?subject=source for item on devdriven.by');
        $("#the-source").html('<i class="fa fa-question-circle"></i>');
    }

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

    ga('send', 'pageview');
}

function onTweetClick(ev) {
    ev.preventDefault();

    link = "https://twitter.com/share";
    link += "?url=" +  encodeURIComponent(window.location.protocol + "//" + window.location.host + $("#the-permalink").attr("href"));
    link += "&text=" + encodeURIComponent('"' + document.title + '" -');
    link += "&via=devdrivenby";

    newwindow = window.open(link, 'Share on Twitter', 'height=450,width=550');
    if (window.focus) {newwindow.focus()}
    return false;
}
