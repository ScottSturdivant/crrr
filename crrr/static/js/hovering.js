$(document).ready(function(){
    $('.happy-tails-container').hover(function() {
        $(this).find('.happy-tails-txt').css('display', 'block');
    }, function() {
        $(this).find('.happy-tails-txt').css('display', 'none');
    })
});

