$(document).ready(function () {
    $(".start_btn").click(function (e) { 
        $(".start_btn").hide();
        $(".loadding_page").show();
        $(".information_page").hide();
        $(".show_page").hide();
        
        $.post("https://fooder.csiejar.xyz/random", {},
            function (data, textStatus, jqXHR) {
                var restaurant_title = data.restaurant_title;
                var restaurant_img_url = data.restaurant_img_url;
                var menu_img_url = data.menu_img_url;
                var menu_text = data.menu_text;
                var prefer_dish_img_url = data.prefer_dish_img_url;
                var prefer_dish_text = data.prefer_dish_text;
                var restaurant_googlemap_link = data.restaurant_googlemap_link;
                
                $("#restaurant_title").html(restaurant_title);
                $("#view_img").prop("src",restaurant_img_url);
                $(".check_menu_page img").prop("src",menu_img_url);
                $("#menu_text").html(menu_text);
                $(".prefer_dish_page img").prop("src",prefer_dish_img_url);
                $("#prefer_dish_text").html(prefer_dish_text);
                $("#restaurant_googlemap_link").prop("href",restaurant_googlemap_link);

                $(".loadding_page").hide();
                $(".show_page").show();
                $(".information_page").show();
                $(".start_btn").show();



            },
            "json"
        );
        
    });
});