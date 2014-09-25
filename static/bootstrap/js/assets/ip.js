/**
 * Created by s7eph4ni3 on 13-11-14.
 */
$(function(){
    $('#action-toggle').click(function(){
        if($(this).prop("checked")){
            $('.action-select').prop("checked",true);
        }else{
            $('.action-select').prop("checked",false);
        }
    });
    $('#go_page').click(function(){
        var go_page = $('.go_page').val();
        if (go_page != ''){
            window.location="/networkcenter/iplist?page="+go_page;
        }else{
            alertify.alert("请输入页码！");
        }
    });
    var options = {
        success: function (data) {
            data = JSON.parse(data);
            if (data.code == 1){
                $('#addidc').fadeOut();
                alertify.alert("添加成功");
                $('#alertify-ok').live("click",function(){
                    window.location=window.location.href;
                });
            }else if (data.code == 0){
                $(".ip").text(data.message['ip']+data.message['iprang']);
                $(".idc").text(data.message['idc']);
                $(".auth").text(data.message['auth']);
                $(".section").text(data.message['section']);
                $("#ipsave").show();
                $(".iprang").text('填写格式:172.16.10.1-100');
            }
        }
    };
    // ajaxForm
    $("#ipform").ajaxForm(options);
    $("#iprangform").ajaxForm(options);
    $("#ipsave").click(function(){
        $(this).hide();
        $(".iprang").text('努力添加中。。。,请稍后！');
    });
});