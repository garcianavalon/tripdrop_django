var map_markers = {};

function initMap(map_id, options) {
  // NOTE(garcianavalon) don't use jQuery to find the map canvas!!
  var map = new google.maps.Map(document.getElementById(map_id), options);
  var geocoder = new google.maps.Geocoder();
  var address_field_id = $('#' + map_id).attr('data-location-for')
  console.log(address_field_id)
  $('#' + address_field_id).on('input', function() {
    console.log('input!')
    var address = $(this).val();
    geocodeAddress(map_id, geocoder, map, address);
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