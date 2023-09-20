 $(document).ready(function() {
    $('.main-sidebar .nav-item').on('click', function(){
    if($(this).hasClass('menu-is-opening menu-open')){
        $(this).removeClass('menu-is-opening menu-open');
        $('.nav-item a').removeClass('active');
    }else{
        $(this).addClass('menu-is-opening menu-open');
         $('.nav-item a').removeClass('active');
         $(this).find('a:first').addClass('active');
    }
    });
 });