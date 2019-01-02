// var map;

// function initMap() {
//     map = new google.maps.Map(document.getElementById('map'), {
//         center: { lat: -34.397, lng: 150.644 },
//         zoom: 8
//     });
// }

// function initMap() {
//     // The location of Uluru
//     var uluru = {lat: -25.344, lng: 131.036};
//     // The map, centered at Uluru
//     var map = new google.maps.Map(
//         document.getElementById('map'), {zoom: 14, center: uluru});
//     // The marker, positioned at Uluru
//     var marker = new google.maps.Marker({position: uluru, map: map});
//   }


//   function init() {
//     var input = document.getElementById('locationTextField');
//     var autocomplete = new google.maps.places.Autocomplete(input);

//     ///Start for getting lat and lang

//     google.maps.event.addListener(autocomplete, 'place_changed',
//        function() {
//           var place = autocomplete.getPlace();
//           var lat = place.geometry.location.lat();
//           var lng = place.geometry.location.lng();
//           document.getElementById("lat").innerHTML = "Lat: "+lat+"<br />Lng: "+lng;
//        }
//     );

//     ////End
// }

// google.maps.event.addDomListener(window, 'load', init);