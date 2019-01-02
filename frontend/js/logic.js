var MAPBOX_KEY = 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg';
var MAPQUEST_API_KEY = "VpY2AF2afXCdfAKEBPGgxnv0tRsF1Rnk";

var map = L.map('map').setView([32.0853, 34.7818], 20);

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
            var lat = resp.results[0].locations[0].latLng.lat;
            var lng = resp.results[0].locations[0].latLng.lng;
            newMap(lat, lng)
            console.log(lat, lng);
            return [lat, lng];
            
        },
        error: function(resp) {
            console.log(resp);
        }
    })
} 

function newMap(lat, lng){
    var map = L.map('map').panto([lat, lng], 20);
}

function submitFunction(event){
    event.preventDefault();
    document.querySelector('#dueDate').validity.badInput
    var address = $('#locationTextField')
    var date = $('#dueDate')
    if (address.val().length > 0){
        console.log('address');
        
        getLongLatFromAddress(address)
    }
}

document.getElementById('submitButton').addEventListener('click',submitFunction);
