$(document).ready(function(){
	$(".announcement-acknowledge a").each(function(counter){
		$(this).click(function(e){
			$.get($(this).attr('href'));
			$(this).parent().parent().parent().fadeOut('fast');
			$(this).parent().parent().parent().remove();	
			$('announcement-block')[0].fadeIn('fast');
			e.stopPropagation();
		});
	});
});
