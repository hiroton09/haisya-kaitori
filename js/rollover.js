// JavaScript Document

/*ロールオーバー*/

overImgClassName = 'swap';
overImgPostfix = '_on';
Event.observe(window, 'load', RN_setMouseOverImages, false);
function RN_setMouseOverImages() {
  var btns = $A(document.getElementsByClassName(overImgClassName));
  btns.each(function (node){
    node.imgsrc = node.src;
    node.imgsrc_over = node.src.replace('.gif', overImgPostfix+'.gif').replace('.jpg', overImgPostfix+'.jpg').replace('.png', overImgPostfix+'.png');
    node.onmouseover = function() { this.src = this.imgsrc_over; };
    node.onmouseout = function() { this.src = this.imgsrc; };
  });
}

