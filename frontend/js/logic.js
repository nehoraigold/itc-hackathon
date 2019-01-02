var MAPBOX_KEY = 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg';
var MAPQUEST_API_KEY = "VpY2AF2afXCdfAKEBPGgxnv0tRsF1Rnk";

var map = L.map('map').setView([32.0853, 34.7818], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg'
}).addTo(map);

function getLongLatFromAddress(address) {
    $.ajax({
        type: "POST",
        url: `http://www.mapquestapi.com/geocoding/v1/address?key=${MAPQUEST_API_KEY}`,
        data: {
            "location": address
        },
        dataType: 'json',
        contentType: 'application/json',
        success: function(resp) {
            console.log(resp)
            var lat = resp.results[0].locations[0].latLng.lat;
            var lng = resp.results[0].locations[0].latLng.lng;
            var street = resp.results[0].locations[0].street;
            goToAddress(lat, lng, street)
        },
        error: function(resp) {
            console.log(resp);
        }
    })
}

function goToAddress(lat, lng, street) {
    var latLng = [lat, lng];
    L.marker(latLng).addTo(map).bindPopup(street).openPopup();
    map.setZoom(20).panTo(latLng);
}

function submitFunction(event) {
    event.preventDefault();
    var address = $("#form").children()[0].value;
    var time = $('#form').children()[1].value;
    getLongLatFromAddress(address);
}

$("#form").submit(submitFunction);