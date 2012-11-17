function update_calendar(url, year, month)
{

		$.post(url, {
			year : year,
			month :month,
		}, function(data) {
			calendar= data.calendar.replace('Mon','Pon');	
			calendar= calendar.replace('Tue','Wt');
			calendar= calendar.replace('Wed','Śr');
			calendar= calendar.replace('Thu','Czw');	
			calendar= calendar.replace('Fri','Pt');	
			calendar= calendar.replace('Sat','Sob');		
			calendar= calendar.replace('Sun','Nd');
	
			calendar= calendar.replace('January','Styczeń');
		    calendar= calendar.replace('February','Luty');
		    calendar= calendar.replace('March','Marzec');
		    calendar= calendar.replace('April','Kwiecień');
		    calendar= calendar.replace('May','Maj');
		    calendar= calendar.replace('June','Czerwiec');
		    calendar= calendar.replace('July','Lipiec');
		    calendar= calendar.replace('August','Sierpień');
		    calendar= calendar.replace('September','Wrzesień');
			calendar= calendar.replace('October','Październik');
			calendar= calendar.replace('November','Listopad');
			calendar= calendar.replace('December','Grudzień') ;
	
			$('#calendar').html(calendar);
			$('#ul_events').html(data.event_list);
		});

}