

function ModalToggle(get_url,post_url,t_id,t_title)
{
var content = '';
$.ajax({ type: "GET", 
url: get_url, 
async: false,
cache: false ,
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
                    async: false,
                    cache: false,
                    success: function(data) {
                        
                        if (data === "success"){
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

function linkWrapper(url_to,url_from)
{
    var content = '';
    $.ajax({ type: "GET", 
    url: url_to, 
    async: false,
    cache: false,
    success : function(data){
        response = JSON.parse(data);
        if (url_from.length === 0)
                url_from = "{{ url 'news_main' }}"
        if (response['error'].length === 0){
            window.location = url_to;
        }
        else{
            window.location = url_from;
            ModalToggle(String(response['error']['url']),String(response['error']['url']),'#form',String(response['error']['title']));
        }
    }
    });
}
