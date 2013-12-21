function updateGalleryImages() {
    var imageContainers = $.each($('.image-container'), function(index, div){
        var gallery_images = [];
        var imageElems = $('div img', this).each(function(j, image){
            var width = $(image).width();
            var height = $(image).height();
            var parentDiv = $(image).parent()[0];

            gallery_images.push({
                originalImage: image,
                width: width,
                height: height,
                parentDiv: parentDiv
            });
        });

        var resized_images = linearPartitionFitPics(gallery_images, {
            containerWidth: $('.image-container').width(),
            preferedImageHeight: parseInt($(window).height() / 2, 10),
            border: 2,
        });

        $.each(gallery_images, function(index, image){
            $(image.parentDiv).height(image.height).width(image.width);
        });
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
