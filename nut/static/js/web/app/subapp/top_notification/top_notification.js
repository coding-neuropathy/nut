
define([
    'libs/Class',
    'jquery',
    'libs/fastdom',
    'underscore',
     'cookie'
], function(
    Class,
    $,
    fastdom,
    _
){
    var TopNotification = Class.extend({
        init: function(){
            this.flag = 0;
            console.log('top notification begin');
            this.initClickBell();
            this.checkBadge();
        },
        initClickBell: function(){
            $('.navbar-collapse .notification-icon').click(this.handleClickBell.bind(this));
        },
        checkBadge:function(){
            if($('.nav-user-actions .badge').length > 0){
                $('.nav-notification-wrapper .notification-round').css({display:'inline-block'});
            }else{
                 $('.nav-notification-wrapper .notification-round').css({display:'none'});
            }
        },
        handleClickBell:function(){

            $('.navbar-collapse .notification-drop-list-wrapper').toggle(this.flag++ % 2 == 0);
            console.log('flag:'+this.flag);
            if(this.flag % 2 == 0){
                console.log('no request');
            }else if($('.notification-drop-list').children('.notification-list-item').length){
               console.log('no request');
            }else{
                this.postAjaxNotification();
            }
        },
        postAjaxNotification:function(){
            console.log('post ajax request');
             $.when(
                    $.ajax({
                        cache:true,
                        type:"get",
                        url: '/message/newmessage/',
                        data:''
                    })
                ).then(
                  this.postSuccess.bind(this),
                 this.postFail.bind(this)
                );
        },
        postSuccess:function(result){
            var status = parseInt(result.status);
            if(status == 1){
                this.hiddenLoadingIcon();
                this.showNotificationItems(result);
            }else{
                this.hiddenLoadingIcon();
                this.showFail(result);
            }
        },
        showNotificationItems:function($ele){
            var ajaxDatas = $ele;
            var notificationItems = _.template($('#notification_item_template').html());
            var datas = {
                objects:ajaxDatas.data,
                notification_length:ajaxDatas.data.length
            };
            for(var i=0;i<datas.notification_length;i++){
                datas.objects[i].actor.avatar = datas.objects[i].actor.avatar.replace('/avatar/','/avatar/52/');
                if( datas.objects[i].type == 'article_dig'){
                    var cover_url = datas.objects[i].target.article_cover;
                    datas.objects[i].target.article_cover = cover_url.replace('/images/','/images/52/');
                    console.log('article after url :'+datas.objects[i].target.article_cover);
                }
                if(datas.objects[i].type != 'user_follow' && datas.objects[i].type != 'article_dig' ){
                    var entity_url = datas.objects[i].target.entity_image;
                    var replaceStr = entity_url.substring(entity_url.lastIndexOf('/'));
                    datas.objects[i].target.entity_image = entity_url.replace(replaceStr,'/52'+replaceStr);
                    console.log('article after url :'+datas.objects[i].target.entity_image);

                }
            }
            $('.notification-drop-list').append(notificationItems(datas));
        },
        showFail:function($ele){
            console.log('ajax data failed.');
        },
        postFail:function(data){
            console.log('request failed.please try again');
        },
        hiddenLoadingIcon:function(){
            $('.notification-loading-icon').hide();
        }

    });

    return TopNotification;
});