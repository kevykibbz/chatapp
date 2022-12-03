$(function(){
  $('.follow-btn').click(function(){
    var followID = $(this).data('follow');
    var profile = $(this).data('profile');
    $button = $(this);

    if ($button.hasClass('following-btn')) {
      $.get('/user/unfollow', {unfollow:followID, profile:profile}, function(data){
        $button.removeClass('following-btn');
        $button.removeClass('unfollow-btn');
        $button.html('<i class="fa fa-user-plus"></i>Follow');
        $('.follow-text').text(data.message)
        $('.count-following').text(data.following);
      });
    }else{
      $.get('/user/follow', {follow:followID, profile:profile}, function(data){
        $button.removeClass('follow-btn');
        $button.addClass('following-btn');
        $button.text('Following');
        $('.follow-text').text(data.message)
        $('.count-following').text(data.following);
      });
    }
  });

  $('.follow-btn').hover(function(){
    $button = $(this);

    if($button.hasClass('following-btn')) {
      $button.addClass('unfollow-btn');
      $button.text('Unfollow');
    }
  }, function(){
    if($button.hasClass('following-btn')) {
      $button.removeClass('unfollow-btn');
      $button.text('Following');
    }
  });
});