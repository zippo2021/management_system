function SendNewGroupData(value)
{
    $.ajax(
    {
        url:            "/event/" + $("#event_id").val() +"/study_groups/new_group",
        dataType:       "json",
        data:           JSON.stringify(value),
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
                var newOption = $("<option>" + data["data"] + "</option>").appendTo($("#groups_list"));
                newOption.click(function()
                {
                    GetGroupInfo(this.value)
                });
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

function SendDeleteGroupData(value)
{
    $.ajax(
    {
        url:            "/event/" + $("#event_id").val() +"/study_groups/delete_group",
        dataType:       "json",
        data:           JSON.stringify(value),
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
                $("option:contains(" + value + ")").remove();
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

function GetGroupInfo(value)
{
    var save_button = $("#call_save_group_button");
    if (!save_button.prop("disabled"))
    {
        ErrorMessage("Save changes before select new group");
    }
    else {
        save_button.prop("disabled", true);
        SendGroupInfoRequest(value);
    }
}

function SendSaveGroupMembersRequest()
{
    var send_data = {};
    send_data["group"] = $("#groups_list option:selected").text();
    send_data["not_in_group"] = [];
    send_data["in_group"] = [];
    var pupils = $("#pupils_list").find("input");
    $.each(pupils, function (key, val)
    {
        if ($(val).prop("checked"))
        {
            send_data["in_group"].push($(val).attr("data-id"));
        }
        else
        {
            send_data["not_in_group"].push($(val).attr("data-id"))
        }
    });
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/study_groups/save_group_members",
        dataType: "json",
        data: JSON.stringify(send_data),
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
                $("#call_save_group_button").prop("disabled", true);
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

function SendGroupInfoRequest(value)
{
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/study_groups/get_group_info",
        dataType: "json",
        data: JSON.stringify(value),
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
                var pupils = $("#pupils_list").find("input");
                pupils.prop("checked", false);
                $.each(pupils, function (key, val)
                {
                    if ($(val).attr("data-id") in data["data"])
                    {
                        $(val).prop("checked", true);
                    }
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

$(document).ready(function()
{
    PrepareAjax();
    $("#call_add_group_button").click(function()
    {
        var modal = new Modal();
        var addWindow = $("#add_window").clone();
        addWindow.removeAttr("hidden");
        addWindow.find("input").val("");
        modal.setTitle("Добавить новую группу");
        modal.getContentElement().append(addWindow);
        modal.setButtons([
        {
            label: 'Добавить',
            callback: function ()
            {
                SendNewGroupData(addWindow.find("input").val());

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

    $("#groups_list").find("option").click(function()
    {
        GetGroupInfo(this.value)
    });

    $("#call_delete_group_button").click(function()
    {
        var val = $("#groups_list option:selected").text();
        if (val == '')
        {
            ErrorMessage("Please, select group");
        }
        else
        {
            SendDeleteGroupData(val);
        }
    });

    $("#pupils_list").find("input").change(function()
    {
        $("#call_save_group_button").prop("disabled", false);
    });

    $("#call_save_group_button").click(function()
    {
        SendSaveGroupMembersRequest();
    });
});