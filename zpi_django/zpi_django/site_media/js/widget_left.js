// FUNKCJE DOTYCZACE LEWYCH WIDGETOW
$(function() { 
	// Po kliknieciu na -/+ schowaj/rozwiń widget i zmień grafikę minus/plus
	$('div.widget_title img').click(function(event){
		event.preventDefault();
		if($(this).attr('class') == 'widget_hide'){
			$(this).removeClass('widget_hide').addClass('widget_show');
		} else {
			$(this).removeClass('widget_show').addClass('widget_hide');
		}
		$(this).parent().next('div').stop(true,true).toggle("blind",'fast');
			
	});
});


$(function() {
	// przeciaganie filtrów
		$( "#sortable, #sortable2" ).sortable({
			revert: true,
		});
});
	