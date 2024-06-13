
var div1 = document.getElementsByClassName('div_home')[0];  
var div2 = document.getElementsByClassName('input_div_on')[0];  
  
// document.addEventListener('wheel', function(event) {  
//     // 使用 requestAnimationFrame 来确保更新在浏览器重绘之前执行  
//     requestAnimationFrame(() => {  
//         // 在 requestAnimationFrame 的回调中重新计算 sourceRect  
//         const sourceRect = div1.getBoundingClientRect();  
//         div2.style.marginTop = sourceRect.bottom + "px";  
//         console.log(sourceRect);  
//     });  
// });

var input = document.getElementById('input1')
input.addEventListener('click',function(){
    div2.style.visibility = 'visible';
    div2.style.marginTop = '-13px';
    div2.style.opacity = '1';
})
document.addEventListener('click', function(event) {
    // 检查点击事件的目标元素是否是.from_go或.close-btn
    if (!div2.contains(event.target) && !div1.contains(event.target)) {
        div2.style.marginTop = '0px';
        div2.style.opacity = '0';
        setTimeout(function() {
            div2.style.visibility = 'hidden'; // 隐藏弹出div   // 两秒后执行
        }, 200);
    }
  });



function updateDistances() {  
    // 获取元素  
    var divall_left = document.querySelector('.div_home_1'); // 注意这里的类名可能与你的HTML不匹配  
    var divall_bomoot = document.querySelector('.divall_bomoot');
    var div1Elements = document.getElementsByClassName('divall_left');
    var div2Elements = document.getElementsByClassName('divall_right');
    // 获取元素的位置和大小信息
    var divall_leftRect = divall_left.getBoundingClientRect();
    var divall_bomootRect = divall_bomoot.getBoundingClientRect();

    // 计算.divall_left距离浏览器底部的距离
    var distanceToBottom = window.innerHeight - divall_leftRect.bottom;  

    // 计算.divall_left和.divall_bomoot之间的距离
    var distanceBetween = Math.abs(divall_bomootRect.top - divall_leftRect.bottom);  

    // 遍历div1Elements并更新它们的height（假设你想要统一更新它们的高度）
    // for (var i = 0; i < div1Elements.length; i++) {
        // 这里你需要决定是基于哪个距离来更新高度
        // 例如，如果你想要基于距离底部的距离来更新，你可以这样做：
        // if (distanceToBottom <= 1000) {
        //     div1Elements[i].style.height = distanceToBottom + 'px';
        // } else if(distanceBetween <= 1000){
            // 如果不是基于距离底部，你可能想要使用其他逻辑或默认值  
            div1Elements[0].style.height = distanceBetween + 'px';
            div2Elements[0].style.height = distanceBetween + 'px'; // 或者其他默认值  
        // }  
    // }  

    // console.log('Distance of .div_home_1 to bottom of viewport:', distanceToBottom); // 注意这里可能应该使用.div_home_1或.divall_left，取决于你的意图  
    // console.log('Distance between .div_home_1 and .divall_bomoot:', distanceBetween); // 同上  
}

// 设置定时器，每隔一段时间更新一次距离
setInterval(updateDistances, 500);

var cent_text = document.getElementsByClassName('cent_text')[0];
var svg_botem = document.getElementsByClassName('svg_botem')[0];
var window_top = document.getElementsByClassName('window_top')[0];
var div_Window_all = document.getElementsByClassName('div_Window_all')[0];
svg_botem.addEventListener('click',function(){
    // div_Window_all.style.visibility = 'visible';
    div_Window_all.style.marginTop = '0px';
    // div_Window_all.style.opacity = '1';
    // div_Window_all.style.animation = 'radius 1.5s ease-in-out forwards'
    // window_top.style.display = 'none';
})


var svg_out = document.getElementById('svg1');
// var div_Window_all_out = document.getElementsByClassName('div_Window_all')[0];
svg_out.addEventListener('click',function(){
    div_Window_all.style.marginTop = '-1000px';
    // div_Window_all.style.opacity = '0';
    // div_Window_all.style.animation = 'radiusout 1.5s ease-in-out forwards'
    // setTimeout(function() {
    //     div_Window_all.style.visibility = 'hidden'; // 隐藏弹出div   // 两秒后执行
    // }, 1000);
})

document.getElementsByClassName('input_seek')[0].addEventListener('submit', function(event) {  
    // 阻止表单的默认提交行为  
    event.preventDefault();})
var home_all_centen = document.getElementsByClassName('div_left_home')[0];
var home_div_centen = document.getElementsByClassName('div_home_all')[0];
var div_left_home_text = document.getElementsByClassName('div_left_home_text')[0];
home_div_centen.addEventListener('click',function(){
    home_all_centen.style.visibility = 'visible';
    div_left_home_text.style.marginLeft = '0px';
    home_all_centen.style.animation = "backgroundson 1s ease-in-out forwards"
})
home_all_centen.addEventListener('click',function(){
    div_left_home_text.style.marginLeft = '-240px';
    home_all_centen.style.animation = "backgroundout 1s ease-in-out forwards"
    setTimeout(function() {  
        home_all_centen.style.visibility = 'hidden'; // 两秒后执行  
    }, 800);
})
window.addEventListener('resize', function(event) {
    var width = window.innerWidth || document.documentElement.clientWidth; // 兼容旧浏览器  
    // 在这里，你可以根据新的宽度值来执行其他操作，如改变样式、调整布局等
    if (width > 1300){
        div_left_home_text.style.marginLeft = '-240px';
        home_all_centen.style.animation = "backgroundout 1s ease-in-out forwards"
        setTimeout(function() {
            home_all_centen.style.visibility = 'hidden'; // 两秒后执行  
        }, 800);
    }
    if(width > 1150){
        div_Window_all.style.marginTop = '-1000px';
    }
    if(width < 910){
        cent_text.style.animation = 'txtb 1s ease-in-out forwards';
    }
    else if(width>910){
        cent_text.style.animation = 'txtd 1s ease-in-out forwards';
    }
});
// var widthxp = window.innerWidth;
// if (widthxp < 910){
//     cent_text.style.animation = 'txtb 1s ease-in-out forwards';
// }

var div_home_right = document.getElementsByClassName('div_home_3')[0];
var my_master = document.getElementsByClassName('my_log')[0];
div_home_right.addEventListener('mouseenter',function(){
    my_master.style.height = '500px'
    // my_master.style.display = 'flex';
    div_home_right.addEventListener('mouseleave',function(){
        my_master.style.height = '0px'
        // my_master.style.display = 'none';
    })
})