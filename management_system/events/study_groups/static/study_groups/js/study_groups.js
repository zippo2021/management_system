function SendNewGroupData(value)
{
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
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
                var groupList = $("#group_list");
                $("<option value='" + data["data"]["id"] + "'>" + data["data"]["name"] + "</option>").appendTo(groupList);
                groupList.val(data["data"]["id"]);
                GetPupils();
            }
        },
        error:          function(jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete:       function()
        {
            indicator.destroy();
        }

    });
}

function SendDeleteGroupData()
{
    var sendData = $("#group_list option:selected").val();
    var indicator = LoadingIndicator('Удаляю группу');
    indicator.show();
    $.ajax(
    {
        url:            "/event/" + $("#event_id").val() +"/study_groups/delete_group",
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
                $("#group_list option[value=" + sendData + "]").remove();
                GetPupils();
            }
        },
        error:          function(jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete:       function()
        {
            indicator.destroy();
        }

    });
}

function SendSaveNewMembersRequest()
{
    var send_data = {};
    send_data["study_group"] = $("#group_list option:selected").val();
    send_data["pupils"] ={};
    send_data["pupils"]["remove_from_group"] = [];
    send_data["pupils"]["add_to_group"] = [];
    $('#pupils_list_out :selected').each(function(i, selected)
    {
        send_data["pupils"]["add_to_group"][i] = $(selected).val();
    });
    if (send_data["pupils"]["add_to_group"].length == 0)
        return;
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
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
                GetPupils();
            }
        },
        error: function (jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete: function ()
        {
            indicator.destroy();
        }
    });
}

function SendRemoveMembersRequest()
{
    var send_data = {};
    send_data["study_group"] = $("#group_list option:selected").val();
    send_data["pupils"] ={};
    send_data["pupils"]["remove_from_group"] = [];
    send_data["pupils"]["add_to_group"] = [];
    $('#pupils_list_in :selected').each(function(i, selected)
    {
        send_data["pupils"]["remove_from_group"][i] = $(selected).val();
    });
    if (send_data["pupils"]["remove_from_group"].length == 0)
        return;
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
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
                GetPupils();
            }
        },
        error: function (jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete: function ()
        {
            indicator.destroy();
        }
    });
}

function GetPupils()
{
    var sendData = $("#group_list option:selected").val();
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/study_groups/get_group_info",
        dataType: "json",
        data: JSON.stringify(sendData),
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
                var pupilsIn = data["data"]["in"];
                var pupilsOut = data["data"]["out"];
                var pupilsListIn = $("#pupils_list_in");
                var pupilsListOut = $("#pupils_list_out");
                pupilsListIn.find("option").remove();
                $.each(pupilsIn, function (key, val)
                {
                    $("<option value='" + val["id"] + "'>" + val["name"] + "</option>").appendTo(pupilsListIn);
                });
                pupilsListOut.find("option").remove();
                $.each(pupilsOut, function (key, val)
                {
                    $("<option value='" + val["id"] + "'>" + val["name"] + "</option>").appendTo(pupilsListOut);
                });
            }
        },
        error: function (jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete: function ()
        {
            indicator.destroy();
        }
    });
}

$(document).ready(function()
{
    PrepareAjax();
    GetPupils();
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

    $("#group_list").change(function()
    {
        GetPupils();
    });

    $("#call_delete_group_button").click(function()
    {
        ConfirmWindow('Вы действительно хотите удалить группу?', SendDeleteGroupData);
    });

    $("#add_to_group_button").click(function()
    {
        SendSaveNewMembersRequest();
    });

    $("#remove_from_group_button").click(function()
    {
        SendRemoveMembersRequest();
    });
});