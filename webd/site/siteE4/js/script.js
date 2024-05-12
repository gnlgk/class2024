$(function () {
    // 슬라이드
    let currentIndex = 0;
    $(".sliderWrap").append($(".slider").first().clone(true));

    setInterval(() => {
        currentIndex++;
        $(".sliderWrap").animate({ marginLeft: -100 * currentIndex + "%" }, 600);

        if (currentIndex == 3) {
            setTimeout(() => {
                $(".sliderWrap").animate({ marginLeft: 0 }, 0);
                currentIndex = 0;
            }, 600)
        }
    }, 3000)

    //메뉴
    $(".nav > ul > li").mouseover(function () {
        $(this).find(">ul").stop().slideDown(600);
    });
    $(".nav > ul > li").mouseout(function () {
        $(this).find(">ul").stop().slideUp(300);
    });

    //팝업
    $(".popup_btn").click(() => {
        $(".popup_view").show();
    })
    $(".popup_close").click(() => {
        $(".popup_view").hide();
    })
})