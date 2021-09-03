$(function () {
    $('.js-btn').on('click', function () {        // js-btnクラスをクリックすると、
      $('.nav-bar , .btn-line').toggleClass('open'); // メニューとバーガーの線にopenクラスをつけ外しする
    })
  });