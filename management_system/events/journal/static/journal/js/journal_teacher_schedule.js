function SetDatepickers()
{
    var startDate = $("#event_start_date").val();
    var endDate = $("#event_end_date").val();
    var fromDate = $("#from");
    var toDate = $("#to");
    fromDate.val(startDate);
    fromDate.datepicker(
    {
        autoclose:      true,
        format:         'dd.mm.yyyy',
        startDate:      startDate,
        endDate:        endDate
    });
    toDate.val(endDate);
    toDate.datepicker(
    {
        autoclose:      true,
        format:         'dd.mm.yyyy',
        startDate:      startDate,
        endDate:        endDate
    });

    fromDate.on('changeDate', function()
    {
        if (fromDate.val() > toDate.val())
        {
            toDate.val(fromDate.val());
        }
        toDate.datepicker("option", "startDate", fromDate.val());
        GetSchedule();
    });

    toDate.on('changeDate', function()
    {
        if (fromDate.val() > toDate.val())
        {
            fromDate.val(toDate.val());
        }
        fromDate.datepicker("option", "endDate", toDate.val());
        GetSchedule();
    });
}

function GetSchedule()
{
    var sendData = {};
    sendData["start_date"] = $("#from").val();
    sendData["end_date"] = $("#to").val();
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/teacher/get_schedule",
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
            $("#schedule").find("table").remove();
            $.each(data['data'], function (key, val)
            {
                var currentTable = $("#lessons_table").clone().removeAttr("hidden").removeAttr("id");
                currentTable.find("#lessons_date").text(key);
                $.each(val, function (id, lesson)
                {
                    currentTable.find("#lessons_data").append(
                        "<tr>" +
                            "<td>" + lesson["start_time"] + "</td>" +
                            "<td>" + lesson["end_time"] + "</td>" +
                            "<td>" + lesson["subject"] + "</td>" +
                            "<td>" + lesson["study_group"] + "</td>" +
                            "<td>" + lesson["place"] + "</td>" +
                        "<tr>"
                    );
                });
                $("#schedule").append(currentTable);
             });
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

$(document).ready(function() {
    PrepareAjax();
    SetDatepickers();
    GetSchedule();
});