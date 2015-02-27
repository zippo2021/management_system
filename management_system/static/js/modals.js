

function ModalToggle(get_url,post_url,t_id,t_title)
{
var content = '';
var modal = new Modal();
$.ajax({ type: "GET", 
url: get_url, 
async: false,
cache: false ,
success : function(text)
{
    content = text;
    modal.setTitle(t_title);
    modal.getContentElement().append(content);
    modal.setButtons([
    {
            id:'send',
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



function ToggleSimpleTextModal(text,title){
    var modal = new Modal();
    modal.setTitle(title);
    modal.getContentElement().append(text);
    modal.setButtons([
    {
        label:"Закрыть",
        callback:function(){
            modal.hide();
            modal.destroy();
        }
    }]);
    modal.show()
}

function linkWrapper(url_to,url_from)
{
    var content = '';
    $.ajax({ type: "GET", 
    url: url_to, 
    async: false,
    cache: false,
    success : function(data){
 
        if (isJson(data)){
            response = JSON.parse(data);
            if (response['error'] != undefined)
                if(typeof response['error'] == 'object')
                    ModalToggle(response['error']['url'],response['error']['url'],'#form',response['error']['title']);
                else
                    ToggleSimpleTextModal(response['error']['text'],'Ошибка доступа');
            else{
				alert('uhi');
                window.location = url_from;
			}
        }
        else{
            var state = {
                "thisIsOnPopState": true
            };

            history.pushState(state, "New Title", url_to);
                     
            document.open();
            document.write(data);
            document.close();
        }    
    },
    error: function(xhr, str){                  
                        ErrorMessage("Error");
                    }
    });
}

function isJson(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

