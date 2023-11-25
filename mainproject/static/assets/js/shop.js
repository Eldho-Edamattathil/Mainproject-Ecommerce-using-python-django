(function ($) {
    'use strict';
    /*Product Details*/
    var productDetails = function () {
        $('.product-image-slider').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: false,
            asNavFor: '.slider-nav-thumbnails',
        });

        $('.slider-nav-thumbnails').slick({
            slidesToShow: 5,
            slidesToScroll: 1,
            asNavFor: '.product-image-slider',
            dots: false,
            focusOnSelect: true,
            prevArrow: '<button type="button" class="slick-prev"><i class="fi-rs-angle-left"></i></button>',
            nextArrow: '<button type="button" class="slick-next"><i class="fi-rs-angle-right"></i></button>'
        });

        // Remove active class from all thumbnail slides
        $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');

        // Set active class to first thumbnail slides
        $('.slider-nav-thumbnails .slick-slide').eq(0).addClass('slick-active');

        // On before slide change match active thumbnail to current slide
        $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
            var mySlideNumber = nextSlide;
            $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');
            $('.slider-nav-thumbnails .slick-slide').eq(mySlideNumber).addClass('slick-active');
        });

        $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
            var img = $(slick.$slides[nextSlide]).find("img");
            $('.zoomWindowContainer,.zoomContainer').remove();
            $(img).elevateZoom({
                zoomType: "inner",
                cursor: "crosshair",
                zoomWindowFadeIn: 500,
                zoomWindowFadeOut: 750
            });
        });
        //Elevate Zoom
        if ( $(".product-image-slider").length ) {
            $('.product-image-slider .slick-active img').elevateZoom({
                zoomType: "inner",
                cursor: "crosshair",
                zoomWindowFadeIn: 500,
                zoomWindowFadeOut: 750
            });
        }
        //Filter color/Size
        $('.list-filter').each(function () {
            $(this).find('a').on('click', function (event) {
                event.preventDefault();
                $(this).parent().siblings().removeClass('active');
                $(this).parent().toggleClass('active');
                $(this).parents('.attr-detail').find('.current-size').text($(this).text());
                $(this).parents('.attr-detail').find('.current-color').text($(this).attr('data-color'));
            });
        });
        //Qty Up-Down
        $('.detail-qty').each(function () {
            var qtyval = parseInt($(this).find('.qty-val').text(), 10);
            $('.qty-up').on('click', function (event) {
                event.preventDefault();
                qtyval = qtyval + 1;
                $(this).prev().text(qtyval);
            });
            $('.qty-down').on('click', function (event) {
                event.preventDefault();
                qtyval = qtyval - 1;
                if (qtyval > 1) {
                    $(this).next().text(qtyval);
                } else {
                    qtyval = 1;
                    $(this).next().text(qtyval);
                }
            });
        });

        $('.dropdown-menu .cart_list').on('click', function (event) {
            event.stopPropagation();
        });
    };
    /* WOW active */
    new WOW().init();

    //Load functions
    $(document).ready(function () {
        productDetails();
    });

})(jQuery);






$(document).ready(function (){
    $(".filter-checkbox").on("click", function(){
        event.preventDefault();
        console.log("A box have been clicked");
        let filter_object ={}
        $(".filter-checkbox").each(function(){
            let filter_value=$(this).val()
            let filter_key = $(this).data("filter")
           

            filter_object[filter_key]=Array.from (document.querySelectorAll('input[data-filter="' + filter_key + '"]:checked')).map(function(element){
                return element.value
            })


        })
        console.log("filter object is: ",filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending data..");

            },
            success:function(response){
                console.log(response);
                console.log('data filtered suessgfuly');

                $("#filtered-product").html(response.data)
                console.log("Response Data:", response.data);

            }

        })

    })    

})

        

// $(document).ready(function() {
//     // Function to update products based on the selected price range
//     function updateProducts(minPrice, maxPrice) {
//         $.ajax({
//             url: '{% url "filter_products" %}',
//             data: { min_price: minPrice, max_price: maxPrice },
//             dataType: 'json',
//             success: function(data) {
//                 // Handle the updated product data
//                 console.log(data.products);
//                 // Implement logic to update the displayed products on the page
//             },
//             error: function(error) {
//                 console.log('Error fetching products:', error);
//             }
//         });
//     }

//     // Event listener for price range changes
//     $('#price-slider').on('slideStop', function(event) {
//         // Get the selected price range
//         var minPrice = event.value[0];
//         var maxPrice = event.value[1];

//         // Update products based on the selected price range
//         updateProducts(minPrice, maxPrice);
//     });
// });

    



