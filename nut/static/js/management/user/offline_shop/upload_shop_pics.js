var OfflineShopManager = Class.extend({
    init: function(){
        console.log('offline shop begin');
        this.initAddPicBtn();
        this.upload_pic_modal_content = $('#add_pic_modal_content').html();
    },

    initAddPicBtn:function(){
        $('#add_pic_button').click(this.show_add_pic_dialog.bind(this));
    },
    show_add_pic_dialog:function(e){
        bootbox.hideAll();
        bootbox.dialog({
            title: '上传商店图片',
            size: 'large',
            onEscape: true,
            backdrop:true,
            closeButton: true,
            animate: true,
            className: 'upload-pic-dialog',
            message:this.upload_pic_modal_content
        });
        //config ZXXFILE object
        var params = {
            fileInput: $("#fileImage").get(0),
            dragDrop: $("#fileDragArea").get(0),
            upButton: $("#fileSubmit").get(0),
            url: $("#uploadForm").attr("action"),
            filter: function(files) {
                var arrFiles = [];
                for (var i = 0, file; file = files[i]; i++) {
                    if (file.type.indexOf("image") == 0) {
                        if (file.size >= 2048000) {
                            bootbox.alert('您这张"'+ file.name +'"图片大小过大，应小于2M');
                        } else {
                            arrFiles.push(file);
                        }
                    } else {
                        bootbox.alert('文件"' + file.name + '"不是图片。');
                    }
                }
                return arrFiles;
            },
            onSelect: function(files) {
                var html = '', i = 0;
                $("#preview").html('<div class="upload_loading"></div>');
                var funAppendImage = function() {
                    file = files[i];
                    if (file) {
                        console.log('file exist >>>');
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            html = html + '<div id="uploadList_'+ i +'" class="upload_append_list"><p><strong>' + file.name + '</strong>'+
                                '<a href="javascript:" class="upload_delete" title="删除" data-index="'+ i +'">删除</a><br />' +
                                '<div class="img-box"><img id="uploadImage_' + i + '" src="' + e.target.result + '" class="upload_image" /></div></p>'+
                                '<span id="uploadProgress_' + i + '" class="upload_progress"></span>' +
                                '</div>';

                            i++;
                            funAppendImage();
                        };
                        reader.readAsDataURL(file);
                    } else {
                        console.log('file none >>>>');
                        $("#preview").html(html);
                        if (html) {
                            //删除方法
                            $(".upload_delete").click(function() {
                                ZXXFILE.funDeleteFile(files[parseInt($(this).attr("data-index"))]);
                                return false;
                            });
                            //提交按钮显示
                            $("#fileSubmit").show();
                        } else {
                            //提交按钮隐藏
                            $("#fileSubmit").hide();
                        }
                    }
                };
                funAppendImage();
            },
            onDelete: function(file) {
                $("#uploadList_" + file.index).fadeOut();
            },
            onDragOver: function() {
                $(this).addClass("upload_drag_hover");
            },
            onDragLeave: function() {
                $(this).removeClass("upload_drag_hover");
            },
            onProgress: function(file, loaded, total) {
                var eleProgress = $("#uploadProgress_" + file.index), percent = (loaded / total * 100).toFixed(2) + '%';
                eleProgress.show().html(percent);
            },
            onSuccess: function(file, response) {
                $("#uploadInf").append("<p>上传成功，图片地址是：" + response + "</p>");
            },
            onFailure: function(file) {
                $("#uploadInf").append("<p>图片" + file.name + "上传失败！</p>");
                $("#uploadImage_" + file.index).css("opacity", 0.2);
            },
            onComplete: function() {
                //提交按钮隐藏
                $("#fileSubmit").hide();
                //file控件value置空
                $("#fileImage").val("");
                $("#uploadInf").append("<p>当前图片全部上传完毕，可继续添加上传。</p>");
            }
        };
        ZXXFILE = $.extend(ZXXFILE, params);
        ZXXFILE.init();
    }

});


(function($, window, document){
    $(function(){
        var sku_manager = new OfflineShopManager();
    });
})(jQuery, window, document);
