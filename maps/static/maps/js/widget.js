function initMap(map_id, options) {
  var map = new google.maps.Map(document.getElementById(map_id), options);
  var geocoder = new google.maps.Geocoder();

  document.getElementById('submit').addEventListener('click', function() {
    geocodeAddress(geocoder, map);
  });
}

function geocodeAddress(geocoder, resultsMap) {
  var address = document.getElementById('address').value;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      resultsMap.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

// init widgets
$(function(){
    $('.map-container').each(function(){
        console.log('check options for map: ', this.id)
        // if there is a variable with the options, initialize the map element
        if (typeof window['options_' + this.id] !== 'undefined') {
            console.log('initialize map: ', this.id)
            initMap($('#' + this.id), window['options_' + this.id]);
        }
    });
})