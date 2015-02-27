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
        format:         'dd/mm/yyyy',
        startDate:      startDate,
        endDate:        endDate
    });
    toDate.val(endDate);
    toDate.datepicker(
    {
        autoclose:      true,
        format:         'dd/mm/yyyy',
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
        UpdateTable();
    });

    toDate.on('changeDate', function()
    {
        if (fromDate.val() > toDate.val())
        {
            fromDate.val(toDate.val());
        }
        fromDate.datepicker("option", "endDate", toDate.val());
        UpdateTable();
    });
}

function UpdateTable()
{
    var sendData = {};
    sendData["start_date"] = $("#from").val();
    sendData["end_date"] = $("#to").val();
     $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/pupil/get_marks",
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
            var pupils = data["data"]["pupils"];
            ClearPupilsTable();
            var pupilList = $("#pupils_list");
            pupilList.val("");
            $.each(pupils, function (key, val)
            {
                $("<tr data-id='" + val["id"] + "'>" +
                    "<td>" + val["name"] + "</td>" +
                  "</tr>").appendTo(pupilList);
            });
            ClearLessonsTable();
            var lessons = data["data"]["lessons"];
            var marks = data["data"]["marks"];
            var lessonsDates = $("#lessons_dates").children().first();
            $.each(lessons, function (key, val)
            {
                $("<td data-id='" + val["id"] + "' title='" + val["title"] + "'>" + val["date"].substring(0, val["date"].lastIndexOf('/')) + "</td>").appendTo(lessonsDates);
            });
            var lessonsLists = $("#lessons_list");
            var pupilsCount = pupilList.children().length;
            var lessonsCount = lessonsDates.children().length;
            for (var i = 1; i <= pupilsCount; i++)
            {
                var tr = "<tr>";
                var pupilId = pupilList.children().eq(i-1).data('id');
                for (var j = 1; j <= lessonsCount; j++)
                {
                    var lessonId = lessonsDates.children().eq(j-1).data('id');
                    tr += "<td>" +
                            "<div>" +
                                "<input type='text' " +
                                    "autocomplete='off' " +
                                    "data-lesson='" + lessonId + "' " +
                                    "data-pupil='" + pupilId + "' " +
                                    "class='mark_input'" +
                                    "value='" + marks[pupilId][lessonId] + "'>" +
                            "</div>" +
                        "</td>";
                }
                tr += "</tr>";
                $(tr).appendTo(lessonsLists);
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

$(document).ready(function() {
    PrepareAjax();
    SetDatepickers();
    UpdateTable();
});