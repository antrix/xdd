$(function() {

    $( "#the-aphorism" ).click(function(ev) {

        ev.preventDefault();

        fetchMoreIfNeeded();

        var ap = Aphorisms.pop();

        if (typeof ap == "undefined") {
            return;
        }

        crossFadeText("#the-aphorism", ap.x);
        crossFadeText("#the-description", ap.desc);

        $("#the-source").attr('href', ap.source);
        $("#the-permalink").attr('href', ap.permalink);

    });

    var fetchInProgress = false;

    function fetchMoreIfNeeded() {
        if (fetchInProgress || Aphorisms.length > 2) {
            return;
        }

        fetchInProgress = true;

        $.ajax({
            dataType: "json",
            cache: false,
            url: "/a/get_random",
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
    $(locator).fadeOut(500, function() {
        $(this).text(text).fadeIn(500);
    });
}
