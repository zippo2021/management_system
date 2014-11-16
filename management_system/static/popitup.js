

function popitup(url) {
  $.ajax({
    url: url,
    success: function(data) {
      $("#dialog-form").load(data).dialog({modal:true}).dialog('open');
    }
  })
  return false;
}


