var markers = {};
var geolocation_callback = undefined;

function initMap(map_id, options) {
  // NOTE(garcianavalon) don't use jQuery to find the map canvas!!
  var map = new google.maps.Map(document.getElementById(map_id), options);
  var geocoder = new google.maps.Geocoder();
  var address_field_id = $('#' + map_id).attr('data-location-for')
  console.log(address_field_id)
  $('#' + address_field_id).on('input', function() {
    var address = $(this).val();
    if (geolocation_callback) {
      window.clearTimeout(geolocation_callback);
    }
    geolocation_callback = window.setTimeout(function(){
      geocodeAddress(map_id, geocoder, map, address);
    }, 1000, map_id, geocoder, map, address);
  });
}

// Sets the map on all markers in the array.
function setMapOnAll(map, map_id) {
  if (!markers[map_id]) {
    markers[map_id] = []
  };
  for (var i = 0; i < markers[map_id].length; i++) {
    markers[map_id][i].setMap(map);
  }
  markers[map_id] = []
}

function geocodeAddress(map_id, geocoder, resultsMap, address) {
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      // clear markers
      setMapOnAll(null, map_id);

      for (var i = results.length - 1; i >= 0; i--) {
        var location = results[i].geometry.location;
        // center
        resultsMap.setCenter(location);

        
        // create new marker
        var marker = new google.maps.Marker({
          map: resultsMap,
          position: location
        });
        markers[map_id].push(marker);
        
      };

      // populate the results field
      $('#id_geolocation_results').val(results);

    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

// init widgets
$(function(){
    $('.map-container').each(function(){
        // if there is a variable with the options, initialize the map element
        if (typeof window['options_' + this.id] !== 'undefined') {
            initMap(this.id, window['options_' + this.id]);
        }
    });
})