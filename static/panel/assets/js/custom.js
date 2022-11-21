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
      },
      success:function(callback)
      {
        
        el.parent().find('button').html(btn_txt).attr('disabled',false);
        if(callback.login)
        {
          if(next)
          {
              window.location=next;
          }
          else
          {
              window.location='/chatroom';
          }
        }

        if(callback.register)
        {
          window.location='/chatroom';
        } 

        if(callback.valid)
        {   
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>'); 
            if(callback.chat)
            {
                el[0].reset();
                el.find("input[aria-label='message']").parents('.wrapper').find('.feedback').css('color','#5cb85c !important').html('<i class="fa fa-check-circle"></i> '+callback.new_message);
                if($('.chat_windows ul').children('li').length > 0)
                {
                  $('.chat_windows ul').append(`<li class="my-message">
                                              <img class="avatar mr-3" src="${callback.profiler}"    alt="${callback.name}">
                                              <div class="message">
                                                  <p class="bg-light-blue">${callback.submitted_message}</p>
                                                  <span class="time" >${callback.time}</span>
                                              </div>
                                          </li>`);
                }
                else
                {
                   $('.chat_windows ul').html(`<li class="my-message">
                                              <img class="avatar mr-3" src="${callback.profiler}"    alt="${callback.name}">
                                              <div class="message">
                                                  <p class="bg-light-blue">${callback.submitted_message}</p>
                                                  <span class="time" >${callback.time}</span>
                                              </div>
                                          </li>`);
                }
                $('.chat_window_list').animate({scrollTop:$(document).height()},'slow');
            }
        }
        else
        {
            $.each(callback.uform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"']").addClass('is-invalid').parent().find('.feedback').addClass('text-danger').html('<span class="fa fa-exclamation-circle"></span> '+value);
            });
            $.each(callback.eform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"']").addClass('is-invalid').parent().find('.feedback').addClass('text-danger').html('<span class="fa fa-exclamation-circle"></span> '+value);
            });

        }
      },
      error:function(err)
      {
        el.parent().find('button').html(btn_txt).attr('disabled',false);
      }
    });
  return false;
});

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const notificationSocket = new WebSocket('ws://'+ window.location.host + '/notification/'+ roomName);
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

      if($('.chat_windows ul').children('li').length > 0)
      {
         $('.chat_windows ul').append(`<li class="other-message">
                                            <img class="avatar mr-3" src="${data.profile}"    alt="${data.name}">
                                            <div class="message">
                                                <p class="bg-light-blue">${data.activity}</p>
                                                <span class="time" >${data.time}</span>
                                            </div>
                                        </li>`);
      }
      else
      {
         $('.chat_windows ul').html(`<li class="other-message">
                                            <img class="avatar mr-3" src="${data.profile}"    alt="${data.name}">
                                            <div class="message">
                                                <p class="bg-light-blue">${data.activity}</p>
                                                <span class="time" >${data.time}</span>
                                            </div>
                                        </li>`);
      }
      $('.chat_window_list').animate({scrollTop:$(document).height()},'slow');
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
   form_data.append('status',is_online)
   url='/update/status';
   $.ajax(
    {
      url:url,
      dataType:'json',
      data:form_data,
      processData:false,
      contentType:false,
      cache:false,
      success:function(callback){},
      error(err)
      {
        console.log(err.status+':'+err.statusText);
      }
    });
}

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