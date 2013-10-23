$(function() {

    $( "#the-aphorism" ).click(function(ev) {

        ev.preventDefault();

        var ap = Aphorisms.pop();

        if (typeof ap == "undefined") {
            return;
        }

        crossFadeText("#the-aphorism", ap.x);
        crossFadeText("#the-description", ap.desc);

        $("#the-source").attr('href', ap.source);
        $("#the-permalink").attr('href', ap.permalink);

    });


});

function crossFadeText(locator, text) {
    $(locator).fadeOut(500, function() {
        $(this).text(text).fadeIn(500);
    });
}
