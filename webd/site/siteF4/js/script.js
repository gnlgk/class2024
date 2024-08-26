
$(function () {
    // 마우스
    $(".nav>ul>li").mouseover(function () {
        $(".nav >ul>li>ul").stop().fadeIn(300);
        $("#header").addClass("on");
    })
    $(".nav>ul>li").mouseout(function () {
        $(".nav >ul>li>ul").stop().fadeOut(100);
        $("#header").removeClass("on");
    })

    // 슬라이더
    let currentIndex = 0;
    $(".sliderWrap").append($(".slider").first().clone(true));

    setInterval(() => {
        currentIndex++;
        $(".sliderWrap").animate({ marginTop: -350 * currentIndex + "px" }, 1000);

        if (currentIndex == 3) {
            $(".sliderWrap").animate({ marginTop: 0 }, 0);
            currentIndex = 0;
        }
    }, 2000);

    //팝업
    $(".popup-btn").click(function () {
        $(".popup").show();
    })
    $(".popup-close").click(function () {
        $(".popup").hide();
    })

})
