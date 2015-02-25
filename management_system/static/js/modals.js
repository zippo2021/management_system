

function ModalToggle(get_url,post_url,t_id,t_title,r_load)
{
var content = '';
$.ajax({ type: "GET", 
url: get_url, 
async: false,
success : function(text)
{
    content = text;
    var modal = new Modal();
    modal.setTitle(t_title);
    modal.getContentElement().append(content);
    modal.setButtons([
    {
            label:'Сохранить',
            callback:function(){
                var msg = modal.getContentElement().find(t_id).serialize();
                $.ajax({
                    type: 'POST',
                    url: post_url,
                    data: msg,
                    success: function(data) {
                        
                        if (data == "success"){
                            modal.hide();
                            modal.destroy();
                            OkMessageAutoClose("Данные сохранены.",2,true);
                        }
                        else{
                            modal.getContentElement().replaceWith("<div class='modal-body'>"+data+"</div>")
                        }
                    },
                    error: function(xhr, str){
                        modal.hide();
                        modal.destroy();
                        ErrorMessage("Error");
                    }
                });
        }
    },
    {
        label:"Закрыть",
        callback:function(){
            modal.hide();
            modal.destroy();
        }
    }]);
    modal.show();
}
});
}


