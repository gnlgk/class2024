$(function () {
    //슬라이드
    let currentIndex = 0;
    $(".sliderWrap").append($(".slider").first().clone(true));

    setInterval(() => {
        currentIndex++;
        $(".sliderWrap").animate({ marginTop: -350 * currentIndex + "px" }, 600);

        if (currentIndex == 3) {
            setTimeout(() => {
                $(".sliderWrap").animate({ marginTop: 0 }, 0);
                currentIndex = 0;
            }, 600)
        }
    }, 3000)
    //메뉴
    $(".nav>ul>li").mouseover(function () {
        $(this).find(">ul").stop().slideDown();
    })
    $(".nav>ul>li").mouseout(function () {
        $(this).find(">ul").stop().slideUp();
    })
    //팝업
    $(".popup_btn").click(function () {
        $(".popup_view").show();
    })
    $(".popup_close").click(function () {
        $(".popup_view").hide();
    })
})