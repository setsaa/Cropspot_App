$(document).ready(function() {
    $('#takePicture').click(function() {
        // Pause the image updating by removing the src attribute
        $('#videoFeed').removeAttr('src');

        // Create and show the loading wheel
        var loadingWheel = $('<div class="loader"></div>');
        $('#videoFeed').replaceWith(loadingWheel);

        $.ajax({
            type: "GET",
            url: "/capture_image",
            success: function(response) {
                var image_path = response.image_path;

                // Redirect to results with image path
                window.location.href = "/results";
            }
        });
    });
});
