/**
 * Created by s7eph4ni3 on 13-12-10.
 */
$(function () {
        $('#id_idc').change(function(){
           var csrftoken = $.cookie('csrftoken');
           var idc_var = $(this).val();
           $.post("/network/apigetrack",{"idc":idc_var, csrfmiddlewaretoken: csrftoken},function(data){
               data = JSON.parse(data);
               if (data.code ==1){
                   $("#id_rack option").remove();
                   $('<option value="" selected="selected">---------</option>').prependTo('#id_rack');
                   for (var i=0;i< data.message.length;i++){
                       var html = '<option value="'+data.message[i].id+'">'+data.message[i].name+'</option>'
                       $(html).prependTo('#id_rack');
                   }
               }else{
                   $("#id_rack option").remove();
                   $('<option value="" selected="selected">---------</option>').prependTo('#id_rack');
               }
           });
       });
       $('#id_rack').change(function(){
           if ($('#id_idc').val() != ''){
               var csrftoken = $.cookie('csrftoken');
               var rack_var = $(this).val();
               $.post("/network/apigetposition",{"rack":rack_var, csrfmiddlewaretoken: csrftoken},function(data){
                   data = JSON.parse(data);
                   if (data.code ==1){
                       $("#id_position option").remove();
                       $('<option value="" selected="selected">---------</option>').prependTo('#id_position');
                       for (var i=0;i< data.message.length;i++){
                           var html = '<option value="'+data.message[i].id+'">'+data.message[i].name+'</option>'
                           $(html).prependTo('#id_position');
                       }
                   }else{
                       $("#id_position option").remove();
                       $('<option value="" selected="selected">---------</option>').prependTo('#id_position');
                   }
               });
           }else{
               alertify.alert("请选择机房！");
               $("#id_rack option").remove();
           }
       });
       $('#id_position').change(function(){
           if ($('#id_rack').val() == ''){
               alertify.alert("请选择机柜！");
               $("#id_position option").remove();
           }
       });
});
