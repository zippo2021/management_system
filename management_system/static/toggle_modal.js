jQuery(document).ready(function ($) {
    $('.view').click(toggle_regular_modal);
    function toggle_regular_modal() {
        $.ajax({
            type: "GET",
            url: "{% url 'toggle_regular_modal' %}",
            dataType: "html",
            cache: false,
            success: function(data){
                if (data == 'UserData'){
            	    location.reload();
            	}
            }
       });
    }
});
