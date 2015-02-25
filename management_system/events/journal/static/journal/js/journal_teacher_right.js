function ClearLessonsTable()
{
    $("#lessons_list").find("tr").remove();
}

function ClearGroupList()
{
    $("#group_list").find('option').remove();
}

function GetLessons()
{
    var sendData = {};
    sendData["start_date"] = $("#from").val();
    sendData["end_date"] = $("#to").val();
    sendData["group"] = $("#group_list option:selected").val();
    sendData["subject"] = $("#subject_list option:selected").val();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/teacher/get_lessons",
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
                ClearLessonsTable();
                var lessons = data["data"]["lessons"];
                var lessonsList = $("#lessons_list");
                lessonsList.val("");
                $.each(lessons, function (key, val)
                {
                    $("<tr data-lessonid=\"" + val["id"] + "\" data-homeworkid=\"" + val["homework_id"] + "\">" +
                        "<td><a class='edit_lesson' href='#'>e</a></td>" +
                        "<td>" + val["date"] + "</td>" +
                        "<td>" + val["start_time"] + "</td>" +
                        "<td>" + val["end_time"] + "</td>" +
                        "<td>" + val["place"] + "</td>" +
                        "<td>" + val["title"] + "</td>" +
                        "<td style='display:none;'>" + val["comment"] + "</td>" +
                        "<td>" + val["homework"] + "</td>" +
                        "<td style='display:none;'>" + val["homework_comment"] + "</td>" +
                        "<td><a class='edit_homework' href='#'>e</a></td>" +
                    "</tr>").appendTo(lessonsList);
                });
                $(".edit_lesson").click(function()
                {
                    var modal = new Modal();
                    var addWindow = PrepareLessonWindow();
                    var current_line = $(this).parent().parent();

                    var lessonDate = addWindow.find("#lesson_date");
                    lessonDate.val(current_line.children().eq(1).html());

                    var startTime = addWindow.find("#start_time");
                    var endTime = addWindow.find("#end_time");

                    startTime.val(current_line.children().eq(2).html());
                    endTime.timepicker("option", "minTime", startTime.val());
                    endTime.val(current_line.children().eq(3).html());

                    addWindow.find("#lesson_place").val(current_line.children().eq(4).html());

                    addWindow.find("#title").val(current_line.children().eq(5).html());
                    addWindow.find("#comment").val(current_line.children().eq(6).html());

                    modal.setTitle("Редактировать занятие");
                    modal.getContentElement().append(addWindow);
                    modal.setButtons([
                    {
                        label: 'Сохранить',
                        callback: function ()
                        {
                            var data = {
                                'id':           current_line.data("lessonid"),
                                'title':        addWindow.find("#title").val(),
                                'comment':      addWindow.find("#comment").val()
                            };
                            SendUpdateLessonRequest(data);
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
                $(".edit_homework").click(function()
                {
                    var modal = new Modal();
                    var addWindow = $("#edit_homework_window").clone();
                    addWindow.removeAttr("hidden");
                    var current_line = $(this).parent().parent();

                    addWindow.find("#task").val(current_line.children().eq(7).html());
                    addWindow.find("#comment").val(current_line.children().eq(8).html());

                    modal.setTitle("Редактировать домашнее задание");
                    modal.getContentElement().append(addWindow);
                    modal.setButtons([
                    {
                        label: 'Сохранить',
                        callback: function ()
                        {
                            var data = {
                                'id':           current_line.data("homeworkid"),
                                'lesson_id':    current_line.data("lessonid"),
                                'task':         addWindow.find("#task").val(),
                                'comment':      addWindow.find("#comment").val()
                            };
                            SendUpdateHomeworkRequest(data);
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
        GetLessons();
    });

    toDate.on('changeDate', function()
    {
        if (fromDate.val() > toDate.val())
        {
            fromDate.val(toDate.val());
        }
        fromDate.datepicker("option", "endDate", toDate.val());
        GetLessons();
    });
}

function SendUpdateHomeworkRequest(sendData)
{
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/schedule/update_homework_teacher",
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
            GetLessons();
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

function SendUpdateLessonRequest(sendData)
{
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/teacher/update_lesson",
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
            GetLessons();
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

function PrepareLessonWindow()
{
    var addWindow = $("#edit_window").clone();
    addWindow.removeAttr("hidden");

    var startDate = $("#event_start_date").val();
    var endDate = $("#event_end_date").val();

    var lessonDate = addWindow.find("#lesson_date");
    lessonDate.datepicker(
    {
        autoclose:      true,
        format:         'dd/mm/yyyy',
        startDate:      startDate,
        endDate:        endDate
    });

    var startTime = addWindow.find("#start_time");
    var endTime = addWindow.find("#end_time");
    startTime.timepicker(
    {
        'step':         5,
        'timeFormat':   'H:i',
        'maxTime':      '00:00'
    });
    endTime.timepicker(
    {
        'step':         5,
        'timeFormat':   'H:i',
        'showDuration': true,
        'maxTime':      '00:00'
    });

    startTime.on('changeTime', function()
    {
        if (startTime.val() > endTime.val())
        {
            endTime.val(startTime.val());
        }
        endTime.timepicker("option", "minTime", startTime.val());
    });
    return addWindow;
}

function GetGroupsBySubject()
{
    var sendData = {};
    sendData["subject"] = $("#subject_list option:selected").val();
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
                $("<option>" + val["name"] + "</option>").appendTo(groupList);
            });
            GetLessons();
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
    GetLessons();
    $("#subject_list").change(function()
    {
        GetGroupsBySubject();
    });
    $("#group_list").change(function()
    {
        GetLessons();
    });
});