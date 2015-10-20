var map_markers = {};
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

function geocodeAddress(map_id, geocoder, resultsMap, address) {
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      // center
      resultsMap.setCenter(results[0].geometry.location);

      // clear markers
      if(map_markers[map_id]) {
        map_markers[map_id].setMap(null);
      }

      // create new marker
      map_markers[map_id] = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });

      // populate the lat/lon fields
      $('#id_lat').val();
      $('#id_lon').val();

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