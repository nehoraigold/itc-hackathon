var MAPBOX_KEY = 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg';
var MAPQUEST_API_KEY = "VpY2AF2afXCdfAKEBPGgxnv0tRsF1Rnk";

var opacityDiv = $('<div/>');
opacityDiv.addClass('opacityDiv');
$('body').append(opacityDiv);

var logo = $('<div/>');
logo.addClass('bigLogo');
$('body').append(logo);


var map = L.map('map').setView([32.0853, 34.7818], 13);
var reporting = true;

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: MAPBOX_KEY
}).addTo(map);

map.on('click', function (event) {
    if (reporting) {
        deleteMapMarkers();
        createReportMarker(event);
    }
})

function createReportMarker(event) {
    var lat = event.latlng.lat;
    var lng = event.latlng.lng;
    var popup = L.popup({closeButton: false}).setContent(`<button id='report-spot' data-lat='${lat}' data-lng='${lng}'>Report</button>`);
    L.marker([lat,lng]).addTo(map).bindPopup(popup).openPopup();
    $("#report-spot").click(reportSpot)
    map.panTo([lat,lng]);
}

function reportSpot() {
    var lat = $(this).attr('data-lat');
    var lng = $(this).attr('data-lng');
    console.log(lat, lng);
}

function deleteMapMarkers() {
    $(".leaflet-pane").slice(2).empty();
}

function getLongLatAndGoToAddress(address) {
    $.ajax({
        type: "POST",
        url: `http://www.mapquestapi.com/geocoding/v1/address?key=${MAPQUEST_API_KEY}`,
        data: {
            "location": address
        },
        dataType: 'json',
        contentType: 'application/json',
        success: function (resp) {
            var lat = resp.results[0].locations[0].latLng.lat;
            var lng = resp.results[0].locations[0].latLng.lng;
            var street = resp.results[0].locations[0].street;
            goToAddress(lat, lng, street)
        },
        error: function (resp) {
            console.log(resp);
        }
    })
}

function goToAddress(lat, lng, street) {
    clearOpacityDiv();
    deleteMapMarkers();
    var latLng = [lat, lng];
    L.marker(latLng).addTo(map).bindPopup(street).openPopup();
    map.flyTo(latLng);
}

function submitFunction(event) {
    event.preventDefault();
    var address = $("#form").children()[0].value;
    var time = $('#form').children()[1].value;
    getLongLatAndGoToAddress(address);
}

function createPolygon(coordArrayOfArrays) {
    L.polygon(coordArrayOfArrays, { color: "gray" }).addTo(map);
}

function changeReportStatus() {
    clearOpacityDiv();
    reporting = !reporting;
    console.log('reporting!')
}

function clearOpacityDiv() {
    opacityDiv.removeClass('opacityDiv');
    logo.addClass('smallLogo');
    logo.removeClass('bigLogo');
}

$(document).ready(function () {
    $("#form").submit(submitFunction);
    $("#report-flag").click(changeReportStatus);
    $.ajax({
        type: 'GET',
        url: '/get_areas',
        contentType: 'application/json',
        success: function (resp) {
            for (var i = 0; i < resp.polygons.length; i++) {
                createPolygon(resp.polygons[i].coord);
            }
        }
    })
});
