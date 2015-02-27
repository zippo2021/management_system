function GetSubjects()
{
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/admin/get_subjects",
        dataType: "json",
        type: "post",
        contentType: "application/json",
        success: function (data)
        {
            if ('error' in data)
            {
                ErrorMessage("Ошибка во время получения данных", data["error"]);
            }
            else
            {
                var subjectList = $("#subject_list");
                subjectList.find("tr").remove();
                $.each(data["data"], function (key, val)
                {
                    $("<tr data-subjectid='" +val["id"] + "'>" +
                            "<td><a class='del_lesson' href='#'><img src='/static/images/delete.png' alt='delete'  height='20'></a>" +
                            "</td><td>" + val["name"] + "</td></tr>").appendTo(subjectList);
                    });
                    $(".del_lesson").click(function()
                    {
                        var data = $(this).parent().parent().data("subjectid");
                        ConfirmWindow('Вы действительно хотите удалить предмет?', function(){
                            SendDelSubjectRequest(data);
                        });
                    });
            }
        },
        error: function (jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete: function ()
        {
        }
    });
}

function SendDelSubjectRequest(sendData)
{
    $.ajax(
    {
        url:            "/event/" + $("#event_id").val() +"/journal/admin/delete_subject",
        dataType:       "json",
        data:           JSON.stringify(sendData),
        type:           "post",
        contentType:    "application/json",
        success:        function(data)
        {
            if ('error' in data)
            {
                ErrorMessage("Ошибка во время получения данных", data["error"]);
            }
            else
            {
                GetSubjects();
            }
        },
        error:          function(jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete:       function()
        {
        }

    });
}

function SendNewSubjectData(data)
{
    $.ajax(
    {
        url:            "/event/" + $("#event_id").val() +"/journal/admin/add_subject",
        dataType:       "json",
        data:           JSON.stringify(data),
        type:           "post",
        contentType:    "application/json",
        success:        function(data)
        {
            if ('error' in data)
            {
                ErrorMessage("Ошибка во время получения данных", data["error"]);
            }
            else
            {
                GetSubjects();
            }
        },
        error:          function(jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete:       function()
        {
        }
    });
}

$(document).ready(function()
{
    PrepareAjax();
    GetSubjects();
    $("#call_add_subject_button").click(function()
    {
        var modal = new Modal();
        var addWindow = $("#add_window").clone();
        addWindow.removeAttr("hidden");
        addWindow.find("input").val("");
        modal.setTitle("Добавить новый предмет");
        modal.getContentElement().append(addWindow);
        modal.setButtons([
        {
            label: 'Добавить',
            callback: function ()
            {
                SendNewSubjectData(addWindow.find("input").val());

                modal.hide();
                modal.destroy();
            }
        },
        {
            label: 'Закрыть',
            callback: function ()
            {
                //just close it
                modal.hide();
                modal.destroy();
            }
        }
        ]);
        modal.show();
    });
});