function ClearLessonsTable()
{
    $("#lessons_list").find("tr").remove();
}

function GetLessons()
{
    var sendData = {};
    sendData["start_date"] = $("#from").val();
    sendData["end_date"] = $("#to").val();
    sendData["group"] = $("#groups_list option:selected").val();
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/admin/get_lessons",
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
                var lessons = data["data"];
                var lessonsList = $("#lessons_list");
                lessonsList.val("");
                $.each(lessons, function (key, val)
                {
                    $("<tr data-lessonid='" +val["id"] + "'>" +
                        "<td><a class='edit_lesson' href='#'><span class='glyphicon glyphicon-pencil'></span></a>" +
                            "<a class='del_lesson' href='#'><span class='glyphicon glyphicon-remove'></span></a>" +
                        "</td>" +
                        "<td>" + val["date"] + "</td>" +
                        "<td>" + val["start_time"] + "</td>" +
                        "<td>" + val["end_time"] + "</td>" +
                        "<td>" + val["group"] + "</td>" +
                        "<td>" + val["subject"] + "</td>" +
                        "<td>" + val["teacher"] + "</td>" +
                        "<td>" + val["place"] + "</td>" +
                    "</tr>").appendTo(lessonsList);
                });
                $(".del_lesson").click(function()
                {
                    var data = $(this).parent().parent().data("lessonid");
                    ConfirmWindow('Вы действительно хотите удалить занятие?', function(){
                        SendDelLessonRequest(data);
                    });
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

                    var subject = current_line.children().eq(5).html();
                    addWindow.find("#subject_list option").filter(function() {
                        return this.text == subject;
                    }).attr('selected', true);

                    var teacher = current_line.children().eq(6).html();
                    addWindow.find("#teacher_list option").filter(function() {
                        return this.text == teacher;
                    }).attr('selected', true);

                    addWindow.find("#lesson_place").val(current_line.children().eq(7).html());

                    modal.setTitle("Редактировать занятие");
                    modal.getContentElement().append(addWindow);
                    modal.setButtons([
                    {
                        label: 'Сохранить',
                        callback: function ()
                        {
                            var data = {
                                'id':           current_line.data("lessonid"),
                                'date':         lessonDate.val(),
                                'start_time':   startTime.val(),
                                'end_time':     endTime.val(),
                                'subject':      addWindow.find("#subject_list option:selected").val(),
                                'teacher':      addWindow.find("#teacher_list option:selected").val(),
                                'place':        addWindow.find("#lesson_place").val()
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
        endDate:        endDate,
        language:       'ru'
    });
    toDate.val(endDate);
    toDate.datepicker(
    {
        autoclose:      true,
        format:         'dd.mm.yyyy',
        startDate:      startDate,
        endDate:        endDate,
        language:       'ru'
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

function SendUpdateLessonRequest(sendData)
{
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/admin/update_lesson",
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
            indicator.destroy();
        }
    });
}

function SendNewLessonRequest(sendData)
{
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/admin/add_lessons",
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
            indicator.destroy();
        }
    });
}

function SendDelLessonRequest(sendData)
{
    var indicator = LoadingIndicator('Обновляю данные');
    indicator.show();
    $.ajax(
    {
        url: "/event/" + $("#event_id").val() + "/journal/admin/del_lesson",
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
        },
        error: function (jqXHR, errorString)
        {
            ErrorMessage("Ошибка во время получения данных", errorString);
        },
        complete: function ()
        {
            indicator.destroy();
            GetLessons();
        }
    });
}

function PrepareLessonWindow()
{
    var addWindow = $("#add_window").clone();
    addWindow.removeAttr("hidden");

    var startDate = $("#event_start_date").val();
    var endDate = $("#event_end_date").val();

    var lessonDate = addWindow.find("#lesson_date");
    lessonDate.datepicker(
    {
        autoclose:      true,
        format:         'dd/mm/yyyy',
        startDate:      startDate,
        endDate:        endDate,
        language:       'ru'
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
        'maxTime':      '23:55'
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

function GetTimesCount(curentWindow)
{
    if (curentWindow.find("#until_list").val() === '1')
    {
        curentWindow.find("#times_list").addClass('hide');
        return;
    }
    var timesList = curentWindow.find("#times_list");
    var step = curentWindow.find("#repeat_list").val();

    timesList.find("option").remove();
    var times = (DayDiff(ParseDate(curentWindow.find("#lesson_date").val()), ParseDate($("#event_end_date").val())) / step | 0) + 1;
    for (var i = 1; i <= times; i++)
    {
        $("<option value='" + i + "'>" + i + "</option>").appendTo(timesList);
    }
    timesList.removeClass("hide");
}

function AddLessonButtonReaction()
{
    $("#call_add_lesson_button").click(function()
    {
        var modal = new Modal();
        var addWindow = PrepareLessonWindow();

        addWindow.find("#repeat_group").removeClass("hide");
        addWindow.find("#repeat_box").change(function(){
            if (this.checked)
            {
                addWindow.find("#repeat_list").removeClass("hide");
                addWindow.find("#until_list").removeClass("hide");
                GetTimesCount(addWindow);
            }
            else
            {
                addWindow.find("#repeat_list").addClass('hide');
                addWindow.find("#until_list").addClass('hide');
                addWindow.find("#times_list").addClass('hide');
            }
        });

        addWindow.find("#repeat_list").change(function(){
            GetTimesCount(addWindow);
        });

        addWindow.find("#until_list").change(function(){
            GetTimesCount(addWindow);
        });

        addWindow.find("#lesson_date").change(function(){
            GetTimesCount(addWindow);
        });

        var lessonDate = addWindow.find("#lesson_date");
        lessonDate.val($("#from").val());

        var startTime = addWindow.find("#start_time");
        var endTime = addWindow.find("#end_time");

        startTime.val("06:00");
        endTime.timepicker("option", "minTime", startTime.val());
        endTime.val("07:30");

        modal.setTitle("Добавить занятие");
        modal.getContentElement().append(addWindow);
        modal.setButtons([
        {
            label: 'Добавить',
            callback: function ()
            {
                var data = {
                    'date':         lessonDate.val(),
                    'start_time':   startTime.val(),
                    'end_time':     endTime.val(),
                    'group':        $("#groups_list option:selected").val(),
                    'subject':      addWindow.find("#subject_list option:selected").val(),
                    'teacher':      addWindow.find("#teacher_list option:selected").val(),
                    'place':        addWindow.find("#lesson_place").val(),
                    'repeat':       addWindow.find("#repeat_box").is(':checked'),
                    'delta':        addWindow.find("#repeat_list").val(),
                    'until':        addWindow.find("#until_list").val(),
                    'times':        addWindow.find("#times_list").val()
                };
                SendNewLessonRequest(data);
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

$(document).ready(function() {
    PrepareAjax();
    SetDatepickers();
    GetLessons();
    AddLessonButtonReaction();
});