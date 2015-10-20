var tripdrop_map = {

  geolocated_marker: undefined,

  init: function() {

    //create variables
    // NOTE(garcianavalon) don't use jQuery to find the map canvas!!
    tripdrop_map.map = new google.maps.Map(document.getElementById('map'), { 
      zoom: 2,
      center: {lat: 4.397, lng: 15.644}
    });

    tripdrop_map.geocoder = new google.maps.Geocoder();
    // bind events
    $('#submit').on('click', function() {
      tripdrop_map.geocode_address();
    });

  },
  geocode_address: function() {
    var address = $('#address').val();
    tripdrop_map.geocoder.geocode({'address': address}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        // center map
        tripdrop_map.map.setCenter(results[0].geometry.location);

        // delete old marker
        if (tripdrop_map.geolocated_marker) {
          tripdrop_map.geolocated_marker.setMap(null);
        }

        // create new marker
        tripdrop_map.geolocated_marker = new google.maps.Marker({
          map: tripdrop_map.map,
          position: results[0].geometry.location
        });

      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
  }

};