$(function() {

    $( "#the-aphorism" ).click(function(ev) {

        ev.preventDefault();

        var ap = Aphorisms.pop();

        if (typeof ap == "undefined") {
            return;
        }

        $("#the-aphorism").text(ap.x);
        $("#the-description").text(ap.desc);
        $("#the-source").attr('href', ap.source);
        $("#the-permalink").attr('href', ap.permalink);

    });


});
