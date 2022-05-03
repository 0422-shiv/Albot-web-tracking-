$(window).scroll(function(){
    if ($(window).scrollTop() >= 50) {
        $('.header-menu').addClass('fixed-header');
        
    }
    else {
        $('.header-menu').removeClass('fixed-header');
       
    }
});
