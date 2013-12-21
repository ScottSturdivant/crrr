function updateGalleryImages() {
    var gallery_images = [];
    var imageElems = $.each($('#image-container div img'), function(index, image){
        var width = $(image).width();
        var height = $(image).height();
        var parentDiv = $(image).parent()[0];
        var p = $(image).parent().parent().find('.happy-tails-txt').find('p')[0];

        gallery_images.push({
            originalImage: image,
            width: width,
            height: height,
            parentDiv: parentDiv,
            p: p
        });
    });

    var resized_images = linearPartitionFitPics(gallery_images, {
        containerWidth: $('#image-container').width(),
        preferedImageHeight: parseInt($(window).height() / 2, 10),
        border: 2,
    });

    $.each(gallery_images, function(index, image){
        $(image.parentDiv).height(image.height).width(image.width);
        $(image.p).css('line-height', image.height+'px');
    });
}

$(window).load(function() {
    updateGalleryImages();
});
$(document).ready(function() {
    updateGalleryImages();
    $(window).resize(function() {
        updateGalleryImages();
    });
});
