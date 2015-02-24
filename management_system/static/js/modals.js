

function ModalToggle(get_url,post_url,t_id,t_title)
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
                        modal.hide();
                        modal.destroy();
                        if (data == "success"){
                            OkMessageAutoClose("Данные сохранены.",2,true);
                        }
                        else
                            ErrorMessage("Error");
                    },
                    error: function(xhr, str){
                        modal.hide();
                        modal.destroy();
                        ErrorWindow("Error");
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

function WizardToggle(get_url,post_url,t_id,t_title)
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
                        modal.hide();
                        modal.destroy();
                        if (data == "success"){
                            OkMessageAutoClose("Данные сохранены.",2,true);
                        }
                        else
                            ErrorMessage("Error");
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
