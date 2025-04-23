$(document).ready(function() {
    console.log("Ready");
    buildCarousel(tire_info);
});

function buildCarousel(data) {
    let carousel = $(`#tire-carousel`);
    console.log(carousel);

    // $(carousel).append(`<div class="test">`)

    let ordered_list = $(`<ol class="carousel_viewport">`);

    for (let index = 0; index < 3; index++) {
        let list_item = $(`<li id="carousel_slide${index} tabindex="${index}" class="carousel__slide">`);
        
        let snapper = $(`<div class="carousel__snapper">`)
        $(list_item).append(snapper)

        let tire_container = $(`<div class="tire-container">`)
        

        $(snapper).append(tire_container)

        let tire_img_container = $(`<div class="tire-img">`)

        $(tire_container).append(tire_img_container)

        let tire_img;
        let tire_description = $(`<div class="tire-description">`);
        if (index > 1)
        {
            // for (let i = 0; i < 3; i++){
            //     tire_img = $(`<img alt="${data["2"]["Slicks"]["Soft"]["color"]} tire" src="../static/images/${data["2"]["Slicks"]["Soft"]["image"]}">`)
            //     $(tire_description).text(data["2"]["Slicks"]["Soft"]["description"])

            //     $(tire_img_container).append(tire_img)
            //     $(tire_img_container).append(tire_description)
    
            //     $(list_item).append(tire_container);
            // }
        } 
        else 
        {
            if (index == 0){
                tire_img = $(`<img src="../static/images/${data["0"]["Wet"]["image"]}">`)
                $(tire_description).text(data["0"]["Wet"]["description"])
            }
            else if (index == 1){
                tire_img = $(`<img src="../static/images/${data["1"]["Intermediate"]["image"]}">`)
                $(tire_description).text(data["1"]["Intermediate"]["description"])
            }

            $(tire_img_container).append(tire_img)
            $(tire_img_container).append(tire_description)

        }

        let prev_link = $(`<a href="#carousel__slide1" class="carousel__prev">`);

        $(prev_link).text("Go to previous slide");

        let next_link = $(`<a href="#carousel__slide1" class="carousel__prev">`);

        $(next_link).text("Go to next slide");
        
        $(list_item).append(prev_link)
        $(list_item).append(next_link)

        ordered_list.append(list_item);
        console.log(ordered_list)
    }

    // let list_item = $(`<li id="carousel__slide1" tabindex="0" class="carousel__slide">`);
    // $(list_item).text("Hello");
    // $(ordered_list).append(list_item);
    $(carousel).prepend(ordered_list)
}