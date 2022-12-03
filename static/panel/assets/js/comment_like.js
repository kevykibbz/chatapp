	$(function(){
		$(document).on('click','.comment-like-btn', function(){
	 		var comment_id  = $(this).data('comment'),
			user_id   = $(this).data('user'),
			counter   = $(this).find('.likesCounter'),
			count     = counter.text();
			button    = $(this);

			$.post('/posting/comment/like', {like:comment_id, user_id:user_id}, function(){
	 			counter.show();
	 			button.addClass('comment-unlike-btn');
				button.removeClass('comment-like-btn');
				count++;
				counter.text(count);
				button.find('.fa-heart-o').addClass('fa-heart');
				button.find('.fa-heart').removeClass('fa-heart-o');
			}); 
		});

	$(document).on('click','.comment-unlike-btn', function(){
 		var comment_id  = $(this).data('comment'),
		user_id   = $(this).data('user'),
		counter   = $(this).find('.likesCounter'),
		count     = counter.text(),
		button    = $(this);

		$.post('/posting/comment/unlike', {unlike:comment_id, user_id:user_id}, function(){
 			counter.show();
 			button.addClass('comment-like-btn');
			button.removeClass('comment-unlike-btn');
			count--;
			if(count === 0){
				counter.hide();
			}else{
			  counter.text(count);
			}
   		    counter.text(count);
			button.find('.fa-heart').addClass('fa-heart-o');
			button.find('.fa-heart-o').removeClass('fa-heart');
		}); 
	});
		
});
