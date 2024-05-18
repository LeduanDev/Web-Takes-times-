
$(document).ready(function () {
    setTimeout(function () {

    });
});
$(window).on('resize', function () {
    setTimeout(function () {

    }, 500);
});
$(".navbar-toggler").click(function () {
    $(".navbar-collapse").slideToggle(250);
    setTimeout(function () {

    });
});

// --------------add active class-on another-page move----------
jQuery(document).ready(function ($) {
    // Get current path and find target link
    var path = window.location.pathname.split("/").pop();

    // Account for home page with empty path
    if (path == '') {
        path = 'index.html';
    }

    var target = $('#navbarSupportedContent ul li a[href="' + path + '"]');
    // Add active class to target link
    target.parent().addClass('active');
});
