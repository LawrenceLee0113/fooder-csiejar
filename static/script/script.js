$(document).ready(function () {
    $(".start_btn").click(function (e) { 
        $(".start_btn").hide();
        $(".loadding_page").show();
        $(".information_page").hide();
        $(".show_page").hide();
        
        $.post("https://fooder.csiejar.xyz/random", {},
            function (data, textStatus, jqXHR) {
                var restaurant_title = data.content.restaurant_title;
                var restaurant_img_url = data.content.restaurant_img_url;
                var menu_img_url = data.content.menu_img_url;
                var menu_text = data.content.menu_text;
                var prefer_dish_img_url = data.content.prefer_dish_img_url;
                var prefer_dish_text = data.content.prefer_dish_text;
                var restaurant_googlemap_link = data.content.restaurant_googlemap_link;
                var restaurant_num = data.content.restaurant_num;
                
               var numstr="#"+restaurant_num;
                 $("#restaurant_title").html(restaurant_title+numstr);
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