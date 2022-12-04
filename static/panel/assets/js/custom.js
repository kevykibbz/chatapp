/*proloader*/
function load()
{
  document.querySelector('.placeholder').style.display="none";
  document.querySelector('.main-display').style.display="block";
}

/*insection observer API */
function observerImages()
{
    var images=document.querySelectorAll('[data-src]'),
    imgOpts={},
    observer=new IntersectionObserver((entries,observer)=>
    {
        entries.forEach((entry)=>
        {
            if(!entry.isIntersecting) return;
            const img=entry.target;
            const newUrl=img.getAttribute('data-src');
            img.src=newUrl;
            observer.unobserve(img);
        });
    },imgOpts);
  
    images.forEach((image)=>
    {
      observer.observe(image)
    });
}

/*ActiveForm*/
$(document).on('submit','.ActiveForm',function()
{
    var el=$(this),
    urlparams=new URLSearchParams(window.location.search),
    next=urlparams.get('next'),
    btn_txt=el.parent().find('button:last').html(),
    form_data=new FormData(this);
    $('.feedback').html('');
    el.children().find('.is-invalid').removeClass('is-invalid');
    $.ajax(
    {
      url:el.attr('action'),
      method:el.attr('method'),
      dataType:'json',
      data:form_data,
      contentType:false,
      cache:false,
      processData:false,
      beforeSend:function()
      {
        el.parent().find('button').html('Please wait...').attr('disabled',true);
        $('#save').html('...').attr('disabled',true);
      },
      success:function(callback)
      {
        el.parent().find('button').html(btn_txt).attr('disabled',false);
        $('#save').html('save').attr('disabled',false);
        if(callback.login){
          if(next){
              window.location=next;
          }else{
              window.location='/dashboard';
          }
        }

        if(callback.chat){
          el[0].reset();
          el.find("textarea[aria-label='message']").removeClass('is-invalid').addClass('is-valid').parent().find('.feedback').removeClass('text-danger').addClass('text-success').html('<span class="fa fa-check-circle"></span> '+callback.new_message);
          if($('.chat_window ul').children('li').length > 0){
              $('.chat_window ul').append(`<li class="clearfix">
                                            <div class="status online message-data text-right">
                                                <span class="time">${callback.time}</span>
                                                <span class="name"  style="color:#50b7f5;">${callback.name?callback.name:callback.current_username}</span>
                                                <i class="zmdi zmdi-circle me"></i>
                                            </div>
                                            <div class="message  my-message float-right"><p>${callback.submitted_message}</p></div>
                                        </li>`);
            }else{
              $('.chat_window ul').html(`<li class="clearfix">
                                            <div class="status online message-data text-right">
                                                <span class="time">${callback.time}</span>
                                                <span class="name"  style="color:#50b7f5;">${callback.name?callback.name:callback.current_username}</span>
                                                <i class="zmdi zmdi-circle me"></i>
                                            </div>
                                            <div class="message  my-message float-right"><p>${callback.submitted_message}</p></div>
                                        </li>`);
            }
            $('.chat_window_list').animate({scrollTop:$(document).height()},'slow');
        }

        if(callback.comment){
          el[0].reset();
          buildComment(el,callback)
        }

        if(callback.username){
          window.location='/welcome/to/the/community';
        } 

        if(callback.retweeted){
          el.find("input[aria-label='retweet_message']").removeClass('is-invalid').addClass('is-valid').parent().find('.feedback').removeClass('text-danger').addClass('text-success').html('<span class="fa fa-check-circle"></span> '+callback.message);
        } 

        if(callback.register){
          window.location='/account/'+callback.email;
        } 

        if(callback.valid){   
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>'); 
            
            if(callback.tweet)
            {
              el[0].reset();
              $('<div class="error-banner"><div class="error-banner-inner"><p id="errorMsg">'+callback.message+'</p></div></div>').insertBefore('.header-wrapper');
              $('.error-banner').hide().slideDown(300).delay(5000).slideUp(300);
              $('.popup-tweet-wrap').hide();
              var elements=$('.tweets').children('.all-tweet').length;
              if(elements < 2){
                buildTweet('html',callback)
              }else{
                buildTweet('prepend',callback)
              }
            }
        }
        else
        {
            $.each(callback.uform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"'],textarea[aria-label='"+key+"']").addClass('is-invalid').parent().find('.feedback').addClass('text-danger').html('<span class="fa fa-exclamation-circle"></span> '+value);
            });
            $.each(callback.eform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"'],textarea[aria-label='"+key+"']").addClass('is-invalid').parent().find('.feedback').addClass('text-danger').html('<span class="fa fa-exclamation-circle"></span> '+value);
            });

        }
      },
      error:function(err)
      {
        el.parent().find('button').html(btn_txt).attr('disabled',false);
        $('#save').html('save').attr('disabled',false);
      }
    });
  return false;
});


$(document).on('change','input[type=file]',function()
{
  $(this).removeClass('is-invalid').addClass('is-valid').parent().find('label').removeClass('invalid-feedback').addClass('valid-feedback').html('Filename: '+this.files[0].name);
}); 

$(document).ready(function ()
{  
    observerImages();
    /*fontname*/
    if(localStorage.getItem("fontname") == 'true')
    {
      $('body').addClass(localStorage.getItem("fontname"));
      $(document).find('input[value="'+localStorage.getItem("fontname")+'"]').prop('checked',true);
    }
    else
    {
      $('body').addClass(localStorage.getItem("fontname"));
      $(document).find('input[value="'+localStorage.getItem("fontname")+'"]').prop('checked',false);
    }
    /*dark-mode*/
    if(localStorage.getItem("darkmode") == 'true')
    {
      $('body').addClass("dark-mode");
      $(document).find('.btn-darkmode').prop('checked',true);
    }
    else
    {
      $('body').removeClass("dark-mode");
      $(document).find('.btn-darkmode').prop('checked',false);
    }

    /*sidebar_dark*/
    if(localStorage.getItem("sidebar")  == 'true')
    {
      $('body').addClass("sidebar_dark");
      $(document).find('.btn-sidebar').prop('checked',true);
    }
    else
    {
      $('body').removeClass("sidebar_dark");
      $(document).find('.btn-sidebar').prop('checked',false);
    }

    /*minsidebar*/
    if(localStorage.getItem("min_sidebar")  == 'true')
    {
      $('#header_top').addClass("dark");
      $(document).find('.btn-min_sidebar').prop('checked',true);
    }
    else
    {
      $('#header_top').removeClass("dark");
      $(document).find('.btn-min_sidebar').prop('checked',false);
    }

    /*iconcolor*/
    if(localStorage.getItem("iconcolor")  == 'true')
    {
      $('body').addClass("iconcolor");
      $(document).find('.btn-iconcolor').prop('checked',true);
    }
    else
    {
      $('body').removeClass("iconcolor");
      $(document).find('.btn-iconcolor').prop('checked',false);
    }

     /*gradient*/
    if(localStorage.getItem("gradient")  == 'true')
    {
      $('body').addClass("gradient");
      $(document).find('.btn-gradient').prop('checked',true);
    }
    else
    {
      $('body').removeClass("gradient");
      $(document).find('.btn-gradient').prop('checked',false);
    }

    /*boxlayout*/
    if(localStorage.getItem("boxlayout")  == 'true')
    {
      $('body').addClass("boxlayout");
      $(document).find('.btn-boxlayout').prop('checked',true);
    }
    else
    {
      $('body').removeClass("boxlayout");
      $(document).find('.btn-boxlayout').prop('checked',false);
    }

    /*boxshadow*/
    if(localStorage.getItem("boxshadow")  == 'true')
    {
      $(document).find('.notification a').addClass("box_shadow");
      $(document).find('.btn-boxshadow').prop('checked',true);
    }
    else
    {
      $(document).find('.notification a').removeClass("box_shadow");
      $(document).find('.btn-boxshadow').prop('checked',false);
    }

    /*fixnavbar*/
    if(localStorage.getItem("fixnavbar")  == 'true')
    {
      $('#page_top').addClass("sticky-top");
      $(document).find('.btn-fixnavbar').prop('checked',true);
    }
    else
    {
      $('#page_top').removeClass("sticky-top");
      $(document).find('.btn-fixnavbar').prop('checked',false);
    }

    /*pageheader*/
    if(localStorage.getItem("pageheader")  == 'true')
    {
      $('#page_top').addClass("top_dark");
      $(document).find('.btn-pageheader').prop('checked',true);
    }
    else
    {
      $('#page_top').removeClass("top_dark");
      $(document).find('.btn-pageheader').prop('checked',false);
    }

    if(localStorage.getItem('intro') == 'true')
    {
      $(document).find('.intro').hide().next().show();
      $('.exam').show();
    }

    if(localStorage.getItem('active_page'))
    {
      $('.exam').show().find('form').not('#'+localStorage.getItem('active_page')).hide();
    }
    else
    {
      $('.exam').find('form').not('form:first').hide();
    }
    $('.exam').find('form:first').append('<div class="float-right"><button class="btn btn-primary btn-round submitBtn" disabled>save answer <i class="ti-arrow-up"></i></button></div>');
    $('.exam').find('form').not('form:first').not('form:last').append('<div class="float-right"> <button class="btn btn-primary btn-round submitBtn" disabled>save answer <i class="ti-arrow-up"></i></button></div>');
    $('.exam').find('form:last').append('<input type="text"name="lastpage" value="1" hidden> <div class="float-right"><button class="btn btn-primary btn-round submitBtn" disabled>save answer <i class="ti-arrow-up"></i></button></div></div>');
    
    $(document).on('change','.exam input[type=radio]',function()
    {
      $(this).parents('form').find('button:last').attr('disabled',false);
      $(this).parents('form').find('input[type=radio]').not(':checked').attr('disabled',true);
    });
});


/*ProfileForm*/
$(document).on('submit','.ProfileImageForm',function()
{
  var el=$(this),
  form_data=new FormData(this);
  $('.feedback').html('');
  $.ajax(
    {
      url:el.attr('action'),
      method:el.attr('method'),
      dataType:'json',
      data:form_data,
      contentType:false,
      cache:false,
      processData:false,
      beforeSend:function()
      {
        $('.uploadBtn').html('<i class="spinner-border spinner-border-sm"></i> Please wait...');
      },
      xhr:function()
      {
        const xhr=new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress',function(e)
        {
          if(e.lengthComputable)
          {
            const percent=Math.round((e.loaded/e.total)*100);
            $('.uploadBtn').html('<i class="spinner-border spinner-border-sm"></i> Uploading '+percent+'% ...').attr('disabled',true);
          }
        });
        return xhr
      },
      success:function(callback)
      {
        $('.uploadBtn').removeClass('uploadBtn').addClass('getprofilepic').html('<i class="ti-camera"></i> Change picture').attr({'type':'button','disabled':false});
        if(callback.valid)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
            el[0].reset();
          }
        else
        {
            $.each(callback.uform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group').find('.feedback').addClass('invalid-feedback').html('<i class="fa fa-exclamation-circle"></i> '+value);
            });
        }
        if(callback.error)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Info');
            $('.small-model').find('.modal-body').html('<div class="text-info text-center"><i class="fas fa-exclamation-triangle"></i> No changes made.</div>');
        }
      },
      error:function(err)
      {
        $('.uploadBtn').removeClass('uploadBtn').addClass('getprofilepic').html('<i class="ti-camera"></i> Change picture').attr({'type':'button','disabled':false});
        console.log(err.status+':'+err.statusText);
      }
    });
  return false;
});

$(document).on('click','.getprofilepic',function()
{
    var el=$(this);
    el.removeClass('getprofilepic').addClass('uploadBtn').html('<i class="spinner-border spinner-border-sm"></i> Please wait...');
    $('#id_profile_pic').click();
});

$(document).on('click','.formuploadBtn',function()
{
    var el=$(this);
    el.attr('disabled',true).html('<i class="spinner-border spinner-border-sm"></i> Please wait...');
    $('#id_profile_pic').click();
});

$(document).on('change','.profile',function()
{
    var el=$(this),
    file=el.get(0).files[0],
    ext=el.val().substring(el.val().lastIndexOf('.')+1).toLowerCase();
    $('.uploadbtn').removeClass('spinner-border spinner-border-sm').addClass('ti-upload');
    if(file && (ext=='jpg' || ext=='png' || ext=='jpeg' || ext=='gif'))
    {
        var reader=new FileReader();
        reader.onload=function(e)
        {
            $('.imagecard').find('img:last').attr('src',reader.result);
            $('.uploadBtn').html('<i class="ti-upload"></i> Upload').attr('type','submit');
            $('.formuploadBtn').html('<i class="ti-camera "></i> Upload picture').attr('disabled',false);
        }
        reader.readAsDataURL(file);
    }
    else
    {
      $('.small-model').modal({show:true});
      $('.small-model').find('.modal-title').text('Warning');
      $('.small-model').find('.modal-body').html('<div class="text-warning text-center"><i class="zmdi zmdi-alert-triangle"></i> Invalid image format</div>');
    }
});

function buildComment(el,callback){
  var output=``;
  $.each(callback.data,function(key,value){
    output+=`<div class="tweet-show-popup-comment-box">
            <div class="tweet-show-popup-comment-inner">
              <div class="tweet-show-popup-comment-head">
                <div class="tweet-show-popup-comment-head-left">
                   <div class="tweet-show-popup-comment-img">
                    <img src="${callback.response.profile}">
                   </div>
                </div>
                <div class="tweet-show-popup-comment-head-right">
                    <div class="tweet-show-popup-comment-name-box">
                    <div class="tweet-show-popup-comment-name-box-name"> 
                      <a href="/${callback.response.username}">${callback.response.name}</a>
                    </div>
                    <div class="tweet-show-popup-comment-name-box-tname">
                      <a href="/${callback.response.username}">@${callback.response.username}</a>
                    </div>
                   </div>
                   <div class="tweet-show-popup-comment-right-tweet">
                      <p><a href="/${callback.response.username}">@${callback.response.username}</a> ${value.comment}</p>
                   </div>
                  <div class="tweet-show-popup-footer-menu">
                    <ul>
                      <li><button><i class="fa fa-share" aria-hidden="true"></i></button></li>
                      <li>
                          <button class="comment-like-btn" data-comment="${value.id}" data-user="1" style="outline:none;">
                            <i class="fa fa-heart" aria-hidden="true"></i>
                                <span class="likesCounter">0</span>
                            </button>
                      </li>
                      <li>
                        <a href="#" class="more"><i class="fa fa-ellipsis-h" aria-hidden="true"></i></a>
                        <ul> 
                           <li>
                              <a class="delete-button" data-url="/delete/comment/${value.id}" href="javascript:void(0);"><label class="deleteComment text-info" data-tweet="{{comment.id}}">Delete Comment</label></a>
                            </li>
                        </ul>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
            <!--TWEET SHOW POPUP COMMENT inner END-->
            </div>`;
  });
  $('#comments').html(output);
  $('#comments_count').html(callback.response.comments_count)
}


$(document).on('click','.delete-button',function()
  {
    var el=$(this),
    url=el.data('url');
    elements=$('.tweets,#comments').children('.all-tweet,.infinite-item').length;
    elements1=$('#comments').children('.infinite-item').length;
    $.ajax(
    {
      url:url,
      dataType:'json',
      beforeSend:function()
      {
        el.html('<i class="spinner-border spinner-border-sm" role="status"></i> Please wait...');
      },
      success:function(callback)
      {
        $('#comments_count').html(callback.comment_count);
        if(elements < 2){
          $('.tweets').html(`<div class="t-show-wrap"><p class="text-center py-5"><b><i class="ti-info-alt text-info"></i> No tweet(s) found</b></p></div>`);
        }else{
          el.parents('.all-tweet').remove();
        }
        if(elements1 < 2){
          $('#comments').html(`<div class="infinite-item tweet-show-popup-comment-box"><div class="tweet-show-popup-comment-inner" ><p class="text-center py-5"><b><i class="ti-info-alt text-info"></i> No comment(s) found</b></p></div></div>`);
        }else{
          el.parents('.infinite-item').remove();
        }
      },
      error(err)
      {
        console.log(err.status+':'+err.statusText);
      }
    });
  });

function buildTweet(action,callback){
  if(action == 'html'){
  $('.tweets').html(`<div class="all-tweet">
                      <div class="t-show-wrap">
                         <div class="t-show-inner">
                              <div class="t-show-popup" data-tweet="${callback.tweet_id}">
                                  <div class="t-show-head">
                                      <div class="t-show-img">
                                          <img src="${callback.response.profile}"/>
                                      </div>
                                      <div class="t-s-head-content ">
                                          <div class="t-h-c-name media-body">
                                              <span><a href="/${callback.response.profile}">${callback.response.name?callback.response.name:callback.response.username}</a></span>
                                              <span>@${callback.response.username}</span> &bull;
                                              <span>just now</span>
                                          </div>
                                          <div class="t-h-c-dis">${callback.tweeted_message}</div>
                                      </div>
                                  </div>
                                  <div class="t-show-body">
                                    <div class="t-s-b-inner">
                                     <div class="t-s-b-inner-in">
                                       <img src="${callback.image?callback.image:''}" class="imagePopup" data-tweet="${callback.tweet_id}"/>
                                     </div>
                                    </div>
                                  </div> 
                              </div>
                              <div class="t-show-footer">
                                  <div class="t-s-f-right">
                                      <ul>
                                          <li>
                                              <button class="commentBtn" data-tweet="${callback.tweet_id}" data-user="${callback.response.user_id}" style="outline:none;"><i class="fa fa-comment" aria-hidden="true"></i>
                                                  <span class="retweetsCount">0</span>
                                              </button>
                                          </li>
                                          <li>
                                              <button class="retweet" data-tweet="${callback.tweet_id}" data-user="${callback.response.user_id}" style="outline:none;"><i class="fa fa-retweet" aria-hidden="true"></i>
                                                  <span class="retweetsCount">0</span>
                                              </button>
                                          </li>
                                          <li>
                                              <button class="like-btn" data-tweet="${callback.tweet_id}" data-user="${callback.response.user_id}" style="outline:none;"><i class="fa fa-heart" aria-hidden="true"></i>
                                                  <span class="likesCounter">0</span>
                                              </button>
                                          </li>
                                          <li>
                                              <a href="#" class="more">
                                                  <i class="fa fa-ellipsis-h" aria-hidden="true" style="outline:none;"></i>
                                              </a>
                                              <ul>
                                                <li><a class="delete-button" data-url="/delete/tweet/${callback.tweet_id}" href="javascript:void(0);"><label class="deleteTweet" data-tweet="${callback.tweet_id}">Delete Tweet</label></a></li>
                                              </ul>
                                          </li>
                                      </ul>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>`);
  }else{
    $('.tweets').prepend(`<div class="all-tweet">
                      <div class="t-show-wrap">
                         <div class="t-show-inner">
                              <div class="t-show-popup" data-tweet="${callback.tweet_id}">
                                  <div class="t-show-head">
                                      <div class="t-show-img">
                                          <img src="${callback.response.profile}"/>
                                      </div>
                                      <div class="t-s-head-content ">
                                          <div class="t-h-c-name media-body">
                                              <span><a href="/${callback.response.profile}">${callback.response.name?callback.response.name:callback.response.username}</a></span>
                                              <span>@${callback.response.username}</span> &bull;
                                              <span>just now</span>
                                          </div>
                                          <div class="t-h-c-dis">${callback.tweeted_message}</div>
                                      </div>
                                  </div>
                                  <div class="t-show-body">
                                    <div class="t-s-b-inner">
                                     <div class="t-s-b-inner-in">
                                       <img src="${callback.image?callback.image:''}" class="imagePopup" data-tweet="${callback.tweet_id}"/>
                                     </div>
                                    </div>
                                  </div> 
                              </div>
                              <div class="t-show-footer">
                                  <div class="t-s-f-right">
                                      <ul>
                                          <li>
                                              <button  class="commentBtn" data-tweet="${callback.tweet_id}" data-user="${callback.response.user_id}" style="outline:none;"><i class="fa fa-comment" aria-hidden="true"></i>
                                                  <span class="retweetsCount">0</span>
                                              </button>
                                          </li>
                                          <li>
                                              <button class="retweet" data-tweet="${callback.tweet_id}" data-user="${callback.response.user_id}" style="outline:none;"><i class="fa fa-retweet" aria-hidden="true"></i>
                                                  <span class="retweetsCount">0</span>
                                              </button>
                                          </li>
                                          <li>
                                              <button class="like-btn" data-tweet="${callback.tweet_id}" data-user="${callback.response.user_id}" style="outline:none;"><i class="fa fa-heart" aria-hidden="true"></i>
                                                  <span class="likesCounter">0</span>
                                              </button>
                                          </li>
                                          <li>
                                              <a href="#" class="more">
                                                  <i class="fa fa-ellipsis-h" aria-hidden="true" style="outline:none;"></i>
                                              </a>
                                              <ul>
                                                <li><a class="delete-button" data-url="/delete/tweet/${callback.tweet_id}" href="javascript:void(0);"><label class="deleteTweet" data-tweet="${callback.tweet_id}">Delete Tweet</label></a></li>
                                              </ul>
                                          </li>
                                      </ul>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>`);
  }
}

$(function(){
  var win = $(window);

  win.scroll(function(){
    if($(document).height() <= (win.height() + win.scrollTop())){
    observerImages();
    }
  });
});


const roomName = JSON.parse(document.getElementById('room-name').textContent);
const notificationSocket = new WebSocket('wss://'+ window.location.host + '/notification/'+ roomName);
notificationSocket.onopen = function(e)
{
  UpdateStatus(is_online=true)
}
notificationSocket.onmessage = function(e)
{
    const data = JSON.parse(e.data);
    if(data.message)
    {
      var audio = new Audio('/static/panel/assets/audio/notification_sound.mp3');
      audio.play();
      $('.chat_window_list').animate({scrollTop:$(document).height()},'slow');
      if($('.chat_window ul').children('li').length > 0)
      {
        $('.chat_window ul').append(`<li class="clearfix">
                                            <div class="status online message-data text-left">
                                                <i class="zmdi zmdi-circle me"></i>
                                                <span class="name"  style="color:#50b7f5;">${data.name?data.name:data.username}</span>
                                                <span class="time">${data.time}</span>
                                            </div>
                                            <div  class="message other-message text-left"><p>${data.activity}</p></div>
                                        </li>`);
      }
      else
      {
         $('.chat_window ul').html(`<li class="clearfix">
                                            <div class="status online message-data text-left">
                                                <i class="zmdi zmdi-circle me"></i>
                                                <span class="name"  style="color:#50b7f5;">${data.name?data.name:data.username}</span>
                                                <span class="time">${data.time}</span>
                                            </div>
                                            <div class="message other-message text-left"><p>${data.activity}</p></div>
                                        </li>`);
      }
    }
};
notificationSocket.onclose = function(e)
{
  UpdateStatus(is_online=false)
  console.error('Notification socket closed unexpectedly');
};

function UpdateStatus(is_online)
{
   var form_data=new FormData()
   $.get('/update/status', {status:is_online,}, function(data){
     console.log(data)
    });
}


$(document).on('click','.chatbtn',function(){
  var user_id=$(this).data('user');
  $('.chat-box').html('<p class="text-center py-5"><i class="spinner-border spinner-border-sm"></i> Loading...</p>')
  $.get('/retrieve/chats', {user_id:user_id}, function(callback){
      $('.chat-box').html(callback);
      $('.chat_window_list').animate({scrollTop:$(document).height()},'slow');
      $('.mobile-sidebar').toggleClass('active');
      $('.message_counter').hide();
  });
});