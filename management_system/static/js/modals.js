

function ModalToggle(get_url,post_url,t_id,t_title,school)
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
                        if (data === "success"|| isJson(data)){
                            if (school === undefined)
                                school = false;
                            if (school){
                                json_data = JSON.parse(data);
                                var id = json_data['school_id'];
                                var tmp = "<option value = '"+id+"'>" + modal.getContentElement().find("#id_name").val() + "</option>";       
                            }
                            modal.hide();
                            modal.destroy();
                            
                            OkMessageAutoClose("Данные сохранены.",2,!school);
                            $("body").addClass("modal-open");
                            if (school)
                                $(".modal-body").find("select").first().append(tmp);
                                $(".modal-body").find("select").first().val(id);
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
            $("body").addClass("modal-open");
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
    var indicator = new LoadingIndicator('Идет загрузка');
    indicator.show();
    $.ajax({ type: "GET", 
    url: url_to, 
    async: false,
    cache: false,
    success : function(data){
        indicator.destroy();
        if (isJson(data)){
            response = JSON.parse(data);
            if (response['error'] != undefined)
                if(typeof response['error'] == 'object')
                    ModalToggle(response['error']['url'],response['error']['url'],'#form',response['error']['title']);
                else
                    ToggleSimpleTextModal(response['error']['text'],'Ошибка доступа');
        }
        else{
            var state = {
                "thisIsOnPopState": true
            };

            history.pushState(state, "New Title", url_to);       
            var new_doc = document.open("text/html","replace");
            new_doc.write(data);
            new_doc.close();
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

