$(document).ready(function() {
	// Initialize Smart Wizard
	$('#wizard').smartWizard({
		onShowStep : map_initialize,
		labelFinish : 'Utwórz wydarzenie',
		labelNext : 'Dalej',
		labelPrevious : "Cofnij",
		enableFinishButton : false,
		keyNavigation : false,
		onLeaveStep : leaveAStepCallback,
		onFinish : onFinishCallback
	});

	function onFinishCallback() {
		if (validateStep3() == true) {
			send();
		}
	}

	function leaveAStepCallback(obj) {
		var step_num = obj.attr('rel');
		isStepValid = true;
		if (step_num == 1) {
			if (validateStep1() == false) {
				isStepValid = false;

				//   		$('#wizard').smartWizard('showMessage','Please correct the errors in step'+step+ ' and click next.');
				$('#wizard').smartWizard('setError', {
					stepnum : 1,
					iserror : true
				});

			} else {
				$('#wizard').smartWizard('setError', {
					stepnum : 1,
					iserror : false
				});
			}
		}
		if (step_num == 2) {
			if (validateStep2() == false) {
				isStepValid = false;
				//   			$('#wizard').smartWizard('showMessage','Please correct the errors in step'+step+ ' and click next.');
				$('#wizard').smartWizard('setError', {
					stepnum : 2,
					iserror : true
				});
			} else {
				$('#wizard').smartWizard('setError', {
					stepnum : 2,
					iserror : false
				});
			}
		}
		if (step_num == 3) {
			if (validateStep2() == false) {
				isStepValid = false;
				//   			$('#wizard').smartWizard('showMessage','Please correct the errors in step'+step+ ' and click next.');
				$('#wizard').smartWizard('setError', {
					stepnum : 2,
					iserror : true
				});
			} else {
				$('#wizard').smartWizard('setError', {
					stepnum : 2,
					iserror : false
				});
			}
		}

		return isStepValid;
	}

	function validateStep1() {

		var isValid = true;

		//walidacja nazwy
		var name = $('#id_name').val();
		if (!name && name.length <= 0) {
			isValid = false;
			$("#name_error").html("wpisz nazwę").show();
		} else {
			$("#name_error").html("").hide();
		}

		//walidacja kategorii
		var cat = $('#id_category').val();
		if (!cat && cat.length <= 0) {
			isValid = false;
			$("#category_error").html("wybierz kategorię").show();
		} else {
			$("#category_error").html("").hide();
		}

		//walidacja poczatku daty
		var date1 = $('#id_start_date_0').val();
		var h1 = $('#id_start_date_1').val();
		var m1 = $('#id_start_date_2').val();

		var date2 = $('#id_end_date_0').val();
		var h2 = $('#id_end_date_1').val();
		var m2 = $('#id_end_date_2').val();

		//godzina
		if (h1 < 0 && h1 > 24) {
			$("#start_error").html("zły format godziny").show();
		} else {
			$("#start_error").html("").hide();
		}

		if (m1 < 0 && m1 > 60) {
			$("#start_error").html("zły format minut").show();
		}

		if (h2 < 0 && h2 > 24) {
			$("#end_error").html("zły format godziny").show();
		} else {
			$("#end_error").html("").hide();
		}

		if (m2 < 0 && m2 > 60) {
			$("#end_error").html("zły format minut").show();
		} else {
			$("#end_error").html("").hide();
		}
		//czy data zak jest po rozpoczecia
		if (date1 > date2 && (date1 == date2 || h1 == h2 || m1 == m2)) {
			isValid = false;
			$("#end_error").html("data zakończenia jest ustawiona przed rozpoczęciem").show();
		} else {
			$("#end_error").html("").hide();
		}
		//czy zostala wprowadzona
		if (date1 == 0 && date2 == 0) {
			isValid = false;
			$("#start_error").html("wprowadź datę").show();
		} else {
			$("#start_error").html("").hide();

		}

		//walidacja cyklicznosci
		var period = $('#id_period').val();
		if (!period && period.length <= 0) {
			isValid = false;
			$("#period_error").html("wybierz cykliczność").show();
		} else {
			$("#period_error").html("").hide();
		}

		//walidacja krotkiego opisu
		var intr = $('#id_introduction').val();
		if (!intr && intr.length <= 0) {
			isValid = false;
			$("#intr_error").html("wpisz krotki opis").show();
		} else {
			$("#intr_error").html("").hide();
		}

		//strona
		var page = $('#id_own_page').val();
		var pattern = new RegExp(/^(http|https|ftp):\/\/[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/)
		console.log(pattern.test(page));
		if (!page && page.length <= 0) {
			isValid = false;
			$("#own_page_error").html("wpisz swoja strone www").show();
		} else {
			$("#own_page_error").html("").hide();
		}

		return isValid;
	}

	function validateStep2() {
		var isValid = true;

		var lat = $('#lat').val();
		var lng = $('#lng').val();
		if (!lat && !lng) {
			isValid = false;
			$("#map_error").html(" <br/><p> Wpisz miejsce swojego wydarzenia </p>").show();
		} else {
			$("#map_error").html("").hide();
		}

		return isValid;
	}

	function validateStep3() {
		var isValid = true;

		var descr = $('#id_description').val();
		if (!descr && descr.length <= 0) {
			isValid = false;
			$("#descr_error").html("wpisz opis").show();
		} else {
			$("descr_error").html("").hide();
		}

		var ticket = $('#id_tickets').val();
		if (!ticket && ticket.length <= 0) {
			isValid = false;
			$("#ticket_error").html("wpisz wartości biletów").show();
		} else {
			$("ticket_error").html("").hide();
		}

		var tags = $('#id_tags-name').val();
		if (!tags && tags.length <= 0) {
			isValid = false;
			$("#tags_error").html("wpisz tagi po przecinku").show();
		} else {
			$("tags_error").html("").hide();
		}

		return isValid;
	}

	function map_initialize(obj) {

		var step_num = obj.attr('rel');
		// get the current step number

		if (step_num == 2) {
			initialize();

		}
	}

});

