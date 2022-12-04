$(function()
{
	$('.search').keyup(function(){
		var search = $(this).val();
		if(search.length > 0){
			$.get('/request/search/form', {search:search}, function(data){
				$('.popupTweet').html(data);
			});
		}else{
			$('.search-result').html("");
		}
	});

	$(document).on('click','.prompt-search',function(){
		var search = $(this).data('search');
		$.get('/request/search/form', {search:search}, function(data){
			$('.popupTweet').html(data);
		});
	});


	$(document).on('keyup','.popup-search',function(){
		var search = $(this).val();
		if(search.length > 0){
			$.get('/user/search', {search:search}, function(data){
				var output=``;
				if(data.search){
					output+=`<ul>`;
					$.each(data.results,function(key,value){
						output+=`<li>
							  		<div class="nav-right-down-inner trend">
										<div class="nav-right-down-left">
											<a href="/${value.username}"><img class="img-responsive" src="/static/panel/assets/images/defaultProfileImage.png" alt="${value.username}"></a>
										</div>
										<div class="nav-right-down-right">
											<div class="nav-right-down-right-headline">
												<a href="/${value.username}"><b>${value.name?value.name:value.username}</b></a><br><span class="text-muted">@${value.username}</span>
											</div>
											<div class="nav-right-down-right-body">
												<button onclick=location.href="/${value.username}" class="new-btn" style="outline:none;">View profile</button>
											</div>
										</div>
									</div> 
								 </li>`;
					});
					output+=`</ul>`;
					$('.search-result-popup').html(output);	
				}else{
					$('.search-result-popup').html("");
				}
			});
		}else{
			$('.search-result-popup').html("");
		}
	});

	$(document).on('keyup', '.search-chat', function(){
		var search = $(this).val();
		if(search.length >0){
			$.get('/search/chat', {search:search}, function(data){
				var mobile_output=``,
				desktop_output=``;
				if(data.search){
					if(window.matchMedia("(max-width:767px)").matches){
						mobile_output+=`<div class="nav-right-down-wrap chat_list"><ul class="user_list list-unstyled mb-0 mt-3">`;
						$.each(data.results,function(key,value){
							mobile_output+=`<li>
		                                <a href="javascript:void(0);" data-user="${value.id}" class='chatbtn'>
		                                	<img class="img-responsive" src="/static/panel/assets/images/defaultProfileImage.png" alt="${value.username}">
		                                	<div class="about">
		                                	 	<div class="name">${value.name?value.name:value.username}</div>
		                                	</div>
		                                </a>
		                            </li>`;
						});
						mobile_output+=`</ul></div>`;
						$('.search-result').html(mobile_output);
					}
					else{
						desktop_output+=`<div class="nav-right-down-wrap"><ul>`;
						$.each(data.results,function(key,value){
							desktop_output+=`<li>
				                                <div class="follow-body trend infinite-item position-relative">
				                                    <div class="follow-img media-inner">
				                                    	<img class="img-responsive" src="/static/panel/assets/images/defaultProfileImage.png" alt="${value.username}">
				                                    </div>
				                                    <div class="fo-co-head media-body name-section">
				                                        <a href="/${value.username}">${value.name?value.name:value.username}</a><span><br>@${value.username}</span>
				                                    </div>
				                                    <div class="chat-button">
				                                        <button data-user="${value.id}" class='f-btn chatbtn'style='outline:none;'><i class='ti-comments'></i> Chat</button>
				                                    </div>
				                                </div>
				                            </li>`;
						});
						desktop_output+=`</ul></div>`;
						$('.search-result').html(desktop_output);	
					}
				}else{
					$('.search-result').html("");
				}
			});
		}else{
			$('.search-result').html("");
		}
	});


	$(document).on('click','.search-result li',function(){
		$('.search-result').html("");
		$('.search-result li').hide();
	});

	$(window).on('resize',function(){
		$('.search-result').html("");
		$('.search-result li').hide();
	});

});
