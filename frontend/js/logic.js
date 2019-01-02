var MAPBOX_KEY = 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg';
var MAPQUEST_API_KEY = "VpY2AF2afXCdfAKEBPGgxnv0tRsF1Rnk";

var opacityDiv = $('<div/>');
opacityDiv.addClass('opacityDiv');
$('body').append(opacityDiv);

var logo = $('<div/>');
logo.addClass('bigLogo');
$('body').append(logo);


var map = L.map('map').setView([32.0853, 34.7818], 15);
var reporting = false;

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
    $($(this)[0].parentNode).html("<span class='reported-text'>Thank You!</span>");
    // console.log(lat, lng);
}

function deleteMapMarkers() {
    var panes = $('.leaflet-pane');
    panes.slice(2,3).empty();
    panes.slice(4).empty();
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
    console.log(coordArrayOfArrays);
    L.polygon(coordArrayOfArrays).addTo(map);
}

function changeReportStatus() {
    clearOpacityDiv();
    reporting = !reporting;
    var mapElement = $("#map");
    if (reporting) {
        mapElement.css({cursor:"pointer"});
    } else {
        mapElement.css({cursor:"grab"});
        deleteMapMarkers();
    }
}

function clearOpacityDiv() {
    opacityDiv.remove();
    logo.addClass('smallLogo');
    logo.removeClass('bigLogo');
}

$("#form").submit(submitFunction);

// Address autocomplete

placeSearch({
    key: `${MAPQUEST_API_KEY}`,
    container: document.querySelector('#search-input'),
    style: false
  });

$(document).ready(function () {
    $("#form").submit(submitFunction);
    $("#report-flag").click(changeReportStatus);
    $.ajax({
        type: 'GET',
        url: '/get_areas',
        dataType:'json',
        success: function (resp) {
            console.log(resp);
            for (var i = 0; i < resp.polygons.length; i++) {
                console.log('creating polygon for ' + resp.polygons[i].Name);
                createPolygon(resp.polygons[i].coords);
            }
        }
    })
});
