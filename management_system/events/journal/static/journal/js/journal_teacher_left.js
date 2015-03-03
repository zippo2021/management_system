function ClearPupilsTable()
{
    $("#pupils_list").find("tr").remove();
}

function ClearLessonsTable()
{
    $("#lessons_list").find("tr").remove();
    $("#lessons_dates").find("tr").find("td").remove();
}

function ClearGroupList()
{
    $("#group_list").find('option').remove();
}

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
    sendData["study_group"] = $("#group_list option:selected").val();
    sendData["subject"] = $("#subject_list option:selected").val();
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
     $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/teacher/get_pupils_lessons_marks",
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
                $("<td data-id='" + val["id"] + "' title='" + val["title"] + "'>" + val["date"].substring(0, val["date"].lastIndexOf('.')) + "</td>").appendTo(lessonsDates);
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
                    tr += "<td class='mark_input_cell'>" +
                            "<div>" +
                                "<input type='text' " +
                                    "autocomplete='off' " +
                                    "data-lesson='" + lessonId + "' " +
                                    "data-pupil='" + pupilId + "' " +
                                    "class='mark_input form-control'" +
                                    "value='" + marks[pupilId][lessonId] + "'>" +
                            "</div>" +
                        "</td>";
                }
                tr += "</tr>";
                $(tr).appendTo(lessonsLists);
            }
            $(".mark_input").keydown(function(e)
            {
                var oldValue = this.value;
                if ((e.keyCode == 49) || (e.keyCode == 97))
                {
                    this.value = '1';
                }
                else if ((e.keyCode == 50) || (e.keyCode == 98))
                {
                    this.value = '2';
                }
                else if ((e.keyCode == 51) || (e.keyCode == 99))
                {
                    this.value = '3';
                }
                else if ((e.keyCode == 52) || (e.keyCode == 100))
                {
                    this.value = '4';
                }
                else if ((e.keyCode == 53) || (e.keyCode == 101))
                {
                    this.value = '5';
                }
                else if ((e.keyCode == 8) || (e.keyCode == 46))
                {
                    this.value = '';
                }
                else
                {
                    return false;
                }
                if (this.value != oldValue)
                {
                    var sendData = {};
                    sendData["lesson"] = $(this).data("lesson");
                    sendData["pupil"] = $(this).data("pupil");
                    sendData["mark"] = this.value;
                    var input = this;
                     $.ajax(
                    {
                        url: "/event/" + $("#event_id").val() + "/journal/teacher/set_mark",
                        dataType: "json",
                        data: JSON.stringify(sendData),
                        type: "post",
                        contentType: "application/json",
                        success: function (data)
                        {
                            if ('error' in data)
                            {
                                ErrorMessage("Ошибка во время получения данных", data["error"]);
                                input.value = oldValue;
                            }
                        },
                        error: function (jqXHR, errorString)
                        {
                            ErrorMessage("Ошибка во время получения данных", errorString);
                            input.value = oldValue;
                        },
                        complete: function ()
                        {
                        }
                    });
                }
                return false;
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

function GetGroupsBySubject()
{
    var sendData = {};
    sendData["subject"] = $("#subject_list option:selected").val();
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/teacher/get_groups",
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
            var groups = data["data"]["groups"];
            ClearGroupList();
            var groupList = $("#group_list");
            groupList.val("");
            $.each(groups, function (key, val)
            {
                $("<option value='" + val["id"] + "'>" + val["name"] + "</option>").appendTo(groupList);
            });
            UpdateTable();
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
    UpdateTable();
    $("#subject_list").change(function()
    {
        GetGroupsBySubject();
    });
    $("#group_list").change(function()
    {
        UpdateTable();
    });
});