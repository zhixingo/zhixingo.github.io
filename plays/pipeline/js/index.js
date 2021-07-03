(function(){
  var stage = 1,
      active = 1,
      levelCount = $('div[class^=level]').length,
      createLevelState = 0;
  setTheme();
  createLevels();
  showLevels();
  
  $('body').on('click','.block',function(){
    var x = $(this).attr('class').replace(/\D+/g,'');
    if(active && x){
      $(this).removeClass('r' + x);
      x++;
      if($(this).hasClass('straight')){
        if(x == 3) x = 1;
      }else if(x == 5){
        x = 1;
      }
      $(this).addClass('r' + x);
      if(!createLevelState){
        combination();
      }else{
        levelStats();
      }
    }
  });
  
  //d
  
  $('#theme').click(function(){
    $('body').toggleClass('light');
    if($('body').attr('class') == 'light') {
      $('#theme').text('关灯');
    }else{
      $('#theme').text('开灯');
    }
    localStorage.setItem('theme', $('body').attr('class'));
  });
  
  function combination() {
    var x = $('.level' + stage).find('.block'), h = '';
    $.each(x, function(i, el) {
      h += $(this).attr('class').replace(/\D+/g,'');
    });
    console.info(h);
    if($('.level' + stage).data('code') == h){
      stage++;
      active = 0;
      setTimeout(function(){
        showLevels();
      },500);
    }
  }
  
  function showLevels() {
    var remove = stage - 1;
    $('#win .text span').text(remove);
    if(stage > levelCount){
      $('#finished').fadeIn();
    }else if(stage > 1){
      $('#win').fadeIn();
      setTimeout(function(){
        $('.level' + remove).remove();
        $('div.level' + stage).show();
        $('#win').fadeOut();
        active = 1;
      },2000);
    }else{
      $('div.level' + stage).fadeIn();
    }
  }
  
  function createLevels() {
    $.each($('div[data-set]'), function(i,el){
      var levelHtml = '';
      var set = $(this).data('set').split('.');
      $.each(set, function(i, el) {
        var style = 'curve';
        if(set[i][0] == 's') style = 'straight';
        if(set[i][0] == 'e') style = 'end';
        if(set[i][0] == 'b') style = '';
        var rotate = ''
        if(set[i][1]) var rotate = 'r' + set[i][1];
        var double = ''
        if(set[i][2]) var double = 'double';
        levelHtml += '<div class="block ' + style + ' ' + double + ' ' + rotate + '"></div>';
      });
      var text = $(this).data('text');
      if(text) levelHtml += '<div class="text">'+text+'</span></div>';
      $(this).append(levelHtml);
    });
  }
  
  function setTheme() {
    if(localStorage.theme == 'light') {
      $('body').addClass('light');
      $('#theme').text('关灯');
    }
  }
  
  function levelStats() {
    var code = '', set = '';
    $.each($('.newLevel .block'),function(i, el){
      var s = $(this).attr('class').split(' ')[1][0];
      if(s != 'b') code += $(this).attr('class').replace(/\D+/g,'');
      var r = Math.floor(Math.random() * 2) + 1;
      if(s != 's') Math.floor(Math.random() * 4) + 1;
      if(s == 'b') r = '';
      set +=  s + r + '.';
    });
    set = set.slice(0, -1);
    $('.stats').html('code: ' + code + ' - Set: ' + set);
  }
  
  $('.toggleCreateLevel').click(function(){
    $('#createLevel .newLevel').empty();
    $('#createLevel').fadeToggle();
    if(!createLevelState){
      createLevelState = 1;
    }else{
      createLevelState = 0;
    }
  });
  
  $('.tools img').click(function(){
    var x = $(this).attr('class');
    $('.newLevel').append('<div class="block ' + x + ' r1"></div>');
  });
})();