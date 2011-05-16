$(document).ready(function(){
	
	/* Mask functions */
    $(".mask_date").each(function(){
        split_date = $(this).val().split("-");
        if (split_date){
            $(this).val(split_date[1] + "/" + split_date[2] + "/" + split_date[0]);
        }
        $(this).mask("99/99/9999");
    });


    /* Calendar and Today date functions */
    var date_html = "<div><a href='#' class='today append-half'>Today</a><a href='#'><img class='calendar' alt='Calendar'></a></div>";
    $(".date_picker").after(date_html);

    var today = new Date();
	var delimiter = {{ profile.date_display }}
    today = pad((today.getMonth()+1), 2) + '/' + pad(today.getDate(),2) + '/' + today.getFullYear();

    $('.today').each(function(){
        var cal_input =$(this).parent().parent().children(':input');
        $(this).click(function(e){
            cal_input.val(today);
            e.preventDefault();
        });
    });
    $('.calendar').each(function(){
        var cal_input = $(this).parent().parent().parent().children(':input');
        var cal = $(this);
        var date_pick = $(this).DatePicker({
            format:'m/d/Y',
            date: cal_input.val(),
            current: cal_input.val(),
            starts: 1,
            position: 'bottom',
            onChange: function(formated, dates){
                cal_input.val(formated);
            }
        });
    });
});
