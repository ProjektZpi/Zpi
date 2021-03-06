			var map;
			var geocoder;
			var current_lat;
			var current_lng;
			var current_city;
			function initialize() {
				var myLatLong = new google.maps.LatLng(9.931238, 76.2673041);
				//ustaw mape
				var myOptions = {
					zoom : 13,
					center : myLatLong,
					mapTypeId : google.maps.MapTypeId.ROADMAP
				};
				$("#lat").val("");
				$("#lng").val("");
				map = new google.maps.Map(document.getElementById('map'), myOptions);
				geocoder = new google.maps.Geocoder();
			}

			function setPosition(lat, lng) {
				//ustaw inputy na lat i lng;
				current_lat = lat;
				current_lng = lng;
				$("#lat").val(lat);
				$("#lng").val(lng);

			}

			function reverseGeocode(latlng) {
				//pobierz adres z wspolrzednych
				geocoder.geocode({
					'latLng' : latlng
				}, function(results, status) {
					if (status == google.maps.GeocoderStatus.OK) {
						if (results[0]) {
							$("#autocomplete").val(results[0].formatted_address);
							for (var j = 0; j < results.length; j++) {
								//			console.log(results[j]);
								if (results[j].types[0] == "locality") {
									current_city = results[j].address_components[0].long_name
									//			console.log(current_city);

								}

							}

							//						alert(city);
						}
					}
				})
			}


			$(document).ready(function() {


				$("#autocomplete").autocomplete({
					source : function(request, response) {
						//co sie stanie jak napiszemy adres
						//konkretne państwo :nie sprawdzone
						//geocoder.geocode( {‘address’: request.term + “, Indonesia”, ‘region’: ‘ID’ },
						//function(results, status) {
						geocoder.geocode({
							'address' : request.term
						}, function(results) {
							response($.map(results, function(item) {
								//			console.log(results);
								for (var j = 0; j < results.length; j++) {
									//		console.log(results[j].address_components.length);
									for (var k = 0; k < results[j].address_components.length; k++) {
										//	console.log(results[j].types[k]);
										if (results[j].address_components[k].types[0] == "locality") {
											current_city = results[j].address_components[k].long_name
											//				console.log(current_city);

										}
									}

								}
								return {
									label : item.formatted_address,
									value : item.formatted_address,
									latitude : item.geometry.location.lat(),
									longitude : item.geometry.location.lng(),
								}

							}))
						})
					},
					select : function(event, ui) {
						//co sie stanie gdy wcisniemy jakiś adres z podpowiedzi
						var location = new google.maps.LatLng(ui.item.latitude, ui.item.longitude);

						//dodaj marker
						marker = new google.maps.Marker({
							map : map,
							draggable : true

						})
						google.maps.event.addListener(marker, "dragend", function(event) {
							//funkcja po przeciagnieciu markeru
							var point = marker.getPosition();

							setPosition(point.lat(), point.lng());
							//pobierz adres z LatLng
							reverseGeocode(point);
						});
						marker.setPosition(location);
						map.setCenter(location);
						setPosition(ui.item.latitude, ui.item.longitude);
						//dodanie mozliwosci wcisniecia przycisku save
						//	$("#save").removeAttr('disabled');

					}
				})
			});
