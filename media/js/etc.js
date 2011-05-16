function createInfoBoxHTML(hoverId,htmlBox){
	$('#' + hoverId).hover(
		function(e){
			$("body").append(htmlBox);
			$(this).mousemove(function(e) {
				var tipY = e.pageY - $(".info-popup").height();
				var tipX = e.pageX - $(".info-popup").width() - 50;
				$(".info-popup").css({'top': tipY, 'left': tipX});
			});
			$(".info-popup").stop(true,true);
			$(".info-popup").fadeIn("fast");
		},
		function(e){
			$(".info-popup").stop(true,true);
			$(".info-popup").fadeOut("fast");
			$(".info-popup").remove();
		}
	);
}

// Allows us to create little box tooltips around the site
function createInfoBox(hoverId,text,extraClass){
	$('#' + hoverId).hover(
		function(e){
			$("body").append("<div class='info-popup'>" + text + "</div>");
			$(this).mousemove(function(e) {
				var left = 16;
				if (($('body').width() / 2) < e.pageX)
					left = -$(".info-popup").width();

				var tipY = e.pageY + 16;
				var tipX = e.pageX + left;
				$(".info-popup").css({'top': tipY, 'left': tipX});
			});
			$(".info-popup").addClass(extraClass);
			$(".info-popup").stop(true,true);
			$(".info-popup").fadeIn("fast");
		},
		function(e){
			$(".info-popup").stop(true,true);
			$(".info-popup").fadeOut("fast");
			$(".info-popup").remove();
		}
	);
}

// Takes a list of images, and preloads them.
function preload(Images) {
	$(Images).each(function(){
		$('<img/>')[0].src = this;
    });
}

$(document).ready(function(){

	//Pass a list of images to be preloaded
	preload([
		'/media/img/summary-hover.jpg',
		'/media/img/stats-hover.jpg',
		'/media/img/journal-hover.jpg',
		'/media/img/friends-hover.jpg'
	]);

	//Hover functions for the menu icons
	$(".menu-icon").mouseover(function() { 
		var src = $(this).attr("src").match(/[^\.]+/) + "-hover.jpg";
		$(this).attr("src", src);
	});

	$(".menu-icon").mouseout(function() {
		var src = $(this).attr("src").replace("-hover", "");
		$(this).attr("src", src);
	});

});
