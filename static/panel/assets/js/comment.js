$(function(){
	$('#postComment').click(function(){
		var comment = $('#commentField').val();
		var tweet_id = $('#commentField').data('tweet');

		$.post('post/comment', {comment:comment,tweet_id:tweet_id}, function(data){
			var html=`<div class="tweet-show-popup-comment-box">
						<div class="tweet-show-popup-comment-inner">
							<div class="tweet-show-popup-comment-head">
								<div class="tweet-show-popup-comment-head-left">
									 <div class="tweet-show-popup-comment-img">
									 	<img src="/static/${data.profile}">
									 </div>
								</div>
								<div class="tweet-show-popup-comment-head-right">
									  <div class="tweet-show-popup-comment-name-box">
									 	<div class="tweet-show-popup-comment-name-box-name"> 
									 		<a href="/${data.username}">${data.name}</a>
									 	</div>
									 	<div class="tweet-show-popup-comment-name-box-tname">
									 		<a href="/${data.username}">@${data.username}</a>
									 	</div>
									 </div>
									 <div class="tweet-show-popup-comment-right-tweet">
									 		<p><a href="/${data.username}">@${data.username}</a> "/${data.comment}</p>
									 </div>
								 	<div class="tweet-show-popup-footer-menu">
										<ul>
											<li><button><i class="fa fa-share" aria-hidden="true"></i></button></li>
											<li>
												<button class="comment-like-btn" data-comment="${data.id}" data-user="1" style="outline:none;">
													<i class="fa fa-heart" aria-hidden="true"></i>
	                                            	<span class="likesCounter">0</span>
	                                        	</button>
											</li>
											<li>
												<a href="#" class="more"><i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
												<ul> 
												   <li>
												   		<a class="delete-button" data-url="/delete/comment/${data.id}" href="javascript:void(0);"><label class="deleteComment text-info" data-tweet="{{comment.id}}">Delete Comment</label></a>
												   	</li>
												</ul>
											</li>
										</ul>
									</div>
								</div>
							</div>
						</div>
						</div>`;
			$('#comments').html(html);
			$('#commentField').val('');
		});
	});
});