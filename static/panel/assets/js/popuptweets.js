$(function(){
	$(document).on('click', '.t-show-popup', function(){
		var tweet_id = $(this).data('tweet'),
		user_id  = $(this).data('user'),
		el=$(this),btn_text=$(this).html();
		el.html('Process...').attr('disabled',true);
		$.get('/request/comment/form', {showpopup:tweet_id,user_id:user_id}, function(data){
			$('.popupTweet').html(data);
			$('.tweet-show-popup-box-cut').click(function(){
				$('.tweet-show-popup-wrap').hide();
			});
		}).done(function(){el.html(btn_text).attr('disabled',false)});
	});
	$(document).on('click','.imagePopup', function(e){
		e.stopPropagation();
		var tweet_id = $(this).data('tweet');
		var user_id  = $(this).data('user');

		$.post('http://localhost/twitter/core/ajax/imagePopup.php', {showImage:tweet_id,user_id:user_id}, function(data){
			$('.popupTweet').html(data);
			$('.close-imagePopup').click(function(){
				$('.img-popup').hide();
			});

		});
	});
});