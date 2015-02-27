function PrepareAjax()
{
    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
}

LoadingIndicator = function (loadingText)
{
    var $backdrop = null;
    var $loaderIndicator = null;

    function init(loadingText) {
        $backdrop = $('<div class="loader-backdrop fade in"></div>').appendTo('BODY').hide();
        $loaderIndicator = $('<div class="loader modal fade in" tabindex="-1" role="dialog" aria-hidden="false"><i class="indicator fa fa-spin fa-spinner"></i><span>' + loadingText +'</span></div>').appendTo('BODY').hide();
    }

    function show() {
        $backdrop.show();
        $loaderIndicator.show();
    }

    function hide() {
        $backdrop.hide();
        $loaderIndicator.hide();
    }

    function destroy() {
        $backdrop.remove();
        $loaderIndicator.remove();
    }

    init(loadingText);

    this.show = show;
    this.hide = hide;
    this.destroy = destroy;
};

Modal = function ()
{
    var hideCallback = null;

    var $modal = $('<div class="modal fade" id="modal-window" tabindex="-1" role="dialog" aria-hidden="true">\
  <div class="modal-dialog">\
    <div class="modal-content">\
      <div class="modal-header">\
        <div class="modal-title">Modal title</div>\
      </div>\
      <div class="modal-body"></div>\
      <div class="modal-footer"></div>\
    </div>\
  </div>\
</div>').appendTo('BODY').modal('hide');
    $modal.on('hidden.bs.modal', function ()
    {
        $(this).data('bs.modal', null);
        $modal.remove();
        $modal = null;
    });

    function show()
    {
        $modal.modal('show');
    }

    function hide()
    {
        if ($.isFunction(hideCallback))
        {
            hideCallback();
        }
        $modal.modal('hide');
    }

    function setHideCallback(value)
    {
        hideCallback = value;
    }

    function setTitle(value)
    {
        $modal.find('.modal-title').html("<p class='lead'>"+value+'</p>' || '');
    }

    function setButtons(values)
    {
        var $buttons = $modal.find('.modal-footer').empty();
        $.each(values || [], function (index, item) {
            var $button = $('<button type="button" class="btn"/>').appendTo($buttons);
            $button.text(item.label || 'Button #' + index).addClass(item.cssClass || '');

            if ($.isFunction(item.callback)) {
                $button.on('click', item.callback);
            }

            if ($button.hasClass('action-close')) {
                $button.attr('data-dismiss', 'modal');
            }
        });
    }

    function destroy()
    {
        hide();
        $(document).trigger('hidden.bs.modal');
    }

    /**
     * @return {jQuery}
     */
    function getWindowElement()
    {
        return $modal;
    }

    /**
     * @return {jQuery}
     */
    function getContentElement()
    {
        return $modal.find('.modal-body');
    }

    // public methods
    this.show = show;
    this.hide = hide;
    this.setTitle = setTitle;
    this.setHideCallback = setHideCallback;
    this.setButtons = setButtons;
    this.destroy = destroy;
    this.getWindowElement = getWindowElement;
    this.getContentElement = getContentElement;
};

ErrorMessage = function (errorText, errorDescription)
{
    function init(errorText, errorDescription) {
        var modal = new Modal();
        modal.setTitle("Ошибка");
        modal.getContentElement().append($("<p class='text-error'>" + errorText + "<p>"));
        if (errorDescription != undefined)
        {
            modal.getContentElement().append($("<a href='#' class='description_button'>Подробно</a><p hidden='hidden' class='description'>" + errorDescription + "<p>"));
            modal.getContentElement().find(".description_button").click(function()
            {
                modal.getContentElement().find(".description").removeAttr("hidden");
            });
        }
        modal.setButtons([
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
    }
    init(errorText, errorDescription);
};

WarningMessage = function (warningText, warningDescription)
{
    function init(warningText, warningDescription) {
        var modal = new Modal();
        modal.setTitle("Внимание");
        modal.getContentElement().append($("<p class='text-warning'>" + warningText + "<p>"));
        if (warningDescription != undefined)
        {
            modal.getContentElement().append($("<a href='#' class='description_button'>Подробно</a><p hidden='hidden' class='description'>" + warningDescription + "<p>"));
            modal.getContentElement().find(".description_button").click(function()
            {
                modal.getContentElement().find(".description").removeAttr("hidden");
            });
        }
        modal.setButtons([
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
    }
    init(warningText, warningDescription);
};

OkMessageAutoClose = function (okText, delay, autoreload)
{
function init(okText, delay, autoreload) {
var modal = new Modal();
modal.setTitle("Успешно!");
modal.getContentElement().append($("<p class='text-success'>" + okText + "<p>"));
delay = delay || 3;
if (autoreload === undefined)
autoreload = false;
setTimeout(function(){
modal.destroy();
if (autoreload)
location.reload();
}, delay * 1000);
modal.show();
}
init(okText, delay, autoreload);
};

OkMessage = function (okText, okDescription)
{
    function init(okText, okDescription) {
        var modal = new Modal();
        modal.setTitle("Успешно!");
        modal.getContentElement().append($("<p>" + okText + "<p>"));
        if (okDescription != undefined)
        {
            modal.getContentElement().append($("<a href='#' class='description_button'>Подробно</a><p hidden='hidden' class='description'>" + okDescription + "<p>"));
            modal.getContentElement().find(".description_button").click(function()
            {
                modal.getContentElement().find(".description").removeAttr("hidden");
            });
        }
        modal.setButtons([
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
    }
    init(okText, okDescription);
};

AjaxRequest = function (url, request_type, data, data_type, content_type, success_callback, error_callback, complete_callback)
{
    function init(url, request_type, data, data_type, content_type, success_callback, error_callback, complete_callback)
    {
        $.ajax(
        {
            url: url,
            dataType: data_type,
            data: data,
            type: request_type,
            contentType: content_type,
            success: function (data)
            {
                if (success_callback != undefined)
                    success_callback(data);
            },
            error: function (jqXHR, errorString)
            {
                if (error_callback != undefined)
                    error_callback(errorString);
            },
            complete: function ()
            {
                if (complete_callback != undefined)
                    complete_callback();
            }
        });
    }
    init(url, request_type, data, data_type, content_type, success_callback, error_callback, complete_callback);
};

PostAjaxRequest = function (url, data, data_type, content_type, success_callback, error_callback, complete_callback)
{
    function init(url, data, data_type, content_type, success_callback, error_callback, complete_callback)
    {
        AjaxRequest(url, 'post', data, data_type, content_type, success_callback, error_callback, complete_callback)
    }
    init(url, data, data_type, content_type, success_callback, error_callback, complete_callback);
};

GetAjaxRequest = function (url, data, data_type, content_type, success_callback, error_callback, complete_callback)
{
    function init(url, data, data_type, content_type, success_callback, error_callback, complete_callback)
    {
        AjaxRequest(url, 'get', data, data_type, content_type, success_callback, error_callback, complete_callback)
    }
    init(url, data, data_type, content_type, success_callback, error_callback, complete_callback);
};

PostJsonAjaxRequest = function (url, data, success_callback, error_callback, complete_callback)
{
    function init(url, data, success_callback, error_callback, complete_callback)
    {
        AjaxRequest(url, 'post', JSON.stringify(data), "json", "application/json", success_callback, error_callback, complete_callback)
    }
    init(url, data, success_callback, error_callback, complete_callback);
};

GetJsonAjaxRequest = function (url, data, success_callback, error_callback, complete_callback)
{
    function init(url, data, success_callback, error_callback, complete_callback)
    {
        AjaxRequest(url, 'get', JSON.stringify(data), "json", "application/json", success_callback, error_callback, complete_callback)
    }
    init(url, data, success_callback, error_callback, complete_callback);
};
