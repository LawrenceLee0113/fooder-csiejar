var authenticationEndpoint = "https://fooder.csiejar.xyz/uploadImage";
function upload(id) {
    var file = document.getElementById(id);
    var formData = new FormData();
    formData.append("file", file.files[0]);
    formData.append("fileName", "abc.jpg");
    formData.append("publicKey", "public_4YpxagNybX9kAXW6yNx8x9XnFX0=");
    // alert("upload success")
    // Let's get the signature, token and expire from server side
    $.ajax({
        url: authenticationEndpoint,
        method: "GET",
        dataType: "json",
        success: function (body) {
            // alert("get my web site key success")
            formData.append("signature", body.signature || "");
            formData.append("expire", body.expire || 0);
            formData.append("token", body.token);

            // Now call ImageKit.io upload API
            $.ajax({
                url: "https://upload.imagekit.io/api/v1/files/upload",
                method: "POST",
                mimeType: "multipart/form-data",
                dataType: "json",
                data: formData,
                processData: false,
                contentType: false,
                error: function (jqxhr, text, error) {
                    console.log(error)
                },
                success: function (body) {
                    // alert("get url success")
                    switch (id) {
                        case "restaurant_img_url_file_btn": {
                            $("#restaurant_img_url").val(body.url);
                            break;
                        }
                        case "menu_img_url_file_btn": {
                            $("#menu_img_url").val(body.url);
                            break;
                        }
                        case "prefer_dish_img_url_file_btn": {
                            $("#prefer_dish_img_url").val(body.url);
                            break;
                        }

                    }
                    changeHintAnimation(1);
                }
            });
            changeHintAnimation(3);
        },

        error: function (jqxhr, text, error) {
            console.log(arguments);
        }
    });
    changeHintAnimation(2);
}
function hide(){
    $(".loadding_page").hide();
}
function changeHintAnimation(status){
    switch(status){
        case 1:{//finish
            $(".loadding_page").css("display","flex");
            $("#hint_status").html("√完成√");
            setTimeout(hide,2000);
            break;
        }
        case 2:{//get private key
            $(".loadding_page").css("display","flex");
            $("#hint_status").html("載入中30%");
            break;
        }
        case 3:{//get url success
            $(".loadding_page").css("display","flex");
            $("#hint_status").html("載入中70%");
            break;
        }
        
    }
}
$(document).ready(function () {
    $("#submit").click(function (e) {//送出
        $(".hint_page").show();

        data = {
            restaurant_title: $("#restaurant_title").val(),
            restaurant_img_url: $("#restaurant_img_url").val(),
            menu_img_url: $("#menu_img_url").val(),
            menu_text: $("#menu_text").val(),
            prefer_dish_img_url: $("#prefer_dish_img_url").val(),
            prefer_dish_text: $("#prefer_dish_text").val(),
            restaurant_googlemap_link: $("#restaurant_googlemap_link").val()
        }
        if(data.restaurant_title == "" ||data.restaurant_img_url == "" ||data.menu_img_url == "" ||data.menu_text == "" ||data.prefer_dish_img_url == "" ||data.prefer_dish_text == "" ||data.restaurant_googlemap_link == ""){
            alert("！！輸入不可為空！！")
        }else{

            $.post("https://fooder.csiejar.xyz/add", data,
                function (data, textStatus, jqXHR) {
                    $(".uploadding").hide();
                    $(".uploaded").show();
                    $(".input_area").hide();
                    
                    $("#restaurant_title").val("")
                    $("#restaurant_img_url").val("")
                    $("#menu_img_url").val("")
                    $("#menu_text").val("")
                    $("#prefer_dish_img_url").val("")
                    $("#prefer_dish_text").val("")
                    $("#restaurant_googlemap_link").val("")
                },
                "json"
            );
        }
        

    });
    $("input[type='file']").change(function (e) {//get img url
        // alert("change succees");
        upload(this.id)


    });
});