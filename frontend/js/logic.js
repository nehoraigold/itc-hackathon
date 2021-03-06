var MAPBOX_KEY = 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg';
var MAPQUEST_API_KEY = "VpY2AF2afXCdfAKEBPGgxnv0tRsF1Rnk";

var opacityDiv = $('<div/>');
opacityDiv.addClass('opacityDiv');
$('body').append(opacityDiv);

var logo = $('<div/>');
logo.addClass('bigLogo');
$('body').append(logo);

var modal = document.getElementById('id01');

var userName = [{ userName: "rebekawa", password: "reb" }]
var infosLogIn = {
    userName: '',
    password: '',
}

function signUp() {
    document.getElementById('id02').style.display = 'none'
    infosLogIn = {
        userName: $('#unameSU').val(),
        password: $('#pswSU').val()
    }

    if (infosLogIn.userName.length < 1 || infosLogIn.password.length < 1) {

        return

    }
    else {
        userName.push(infosLogIn);
        return;

    }


}


function logIn() {

    var newObject = {
        userName: $('#unameLI').val(),
        password: $('#pswLI').val()
    }


    for (var i = 0; i < userName.length; i++) {
        if (userName[i].userName == newObject.userName && userName[i].password == newObject.password) {
            $('.logSign').removeClass('logSign');
            document.getElementById('id01').style.display = 'none';
            var welcome = $('<div/>');
            welcome.addClass('welcomeDiv');
            welcome.text("Welcome " + newObject.userName);
            $('body').append(welcome);
            return;
        }
        else {
            $('#unameLI').css('background-color', 'red');
            $('#pswLI').css('background-color', 'red');
            setTimeout(function () {
                $('#unameLI').css('background-color', 'white');
                $('#pswLI').css('background-color', '#f1f1f1');
            }, 500);
            return;
        }
    }
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Get the modal
var modal2 = document.getElementById('id02');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}


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
    var popup = L.popup({ closeButton: false }).setContent(
        `<button class='report-btn' id='space-found' data-lat='${lat}' data-lng='${lng}'>Space Found</button>
        <button class='report-btn' id='no-space-found' data-lat='${lat}' data-lng='${lng}'>No Luck</button>`
    );
    L.marker([lat, lng]).addTo(map).bindPopup(popup).openPopup();
    $(".report-btn").click(reportSpot)
    map.panTo([lat, lng]);
}

function reportSpot() {
    var button = $(this);
    var lat = button.attr('data-lat');
    var long = button.attr('data-lng');
    var isFound = button.attr('id') === "space-found";
    var date = new Date();
    var timestamp = parseFloat(date.getHours() + (date.getMinutes() / 60));
    var new_data = {
        lat: lat,
        long: long,
        timestamp: timestamp,
        is_found: isFound
    };
    $.ajax({
        type: "POST",
        url: "/report",
        dataType: "json",
        contentType: "application/json",
        data: new_data,
        success: function(resp) {
            $(button[0].parentNode).html("<div class='reported-text'>Thank You!</div>");
        }
    })
}

function deleteMapMarkers() {
    var panes = $('.leaflet-pane');
    panes.slice(2, 3).empty();
    panes.slice(4).empty();
}

function getLongLatAndGoToAddress(address) {
    //overlay with loading gif?
    $.ajax({
        type: "POST",
        url: `http://www.mapquestapi.com/geocoding/v1/address?key=${MAPQUEST_API_KEY}`,
        data: {
            "location": address
        },
        dataType: 'json',
        contentType: 'application/json',
        success: function (resp) {
            //remove overlay?
            if (resp.results[0].locations.length !== 0) {
                var lat = resp.results[0].locations[0].latLng.lat;
                var lng = resp.results[0].locations[0].latLng.lng;
                var street = resp.results[0].locations[0].street;
                goToAddress(lat, lng, street)
            } else {
                //if no results appear?
            }
        },
        error: function (resp) {
            console.log(resp);
        }
    })
}

function goToAddress(lat, lng, street) {
    clearOpacityDiv();
    deleteMapMarkers();
    getTableData(lat, lng)
    var latLng = [lat, lng];
    L.marker(latLng).addTo(map).bindPopup(street).openPopup();
    map.flyTo(latLng);
    addTable();
}

function submitFunction(event) {
    event.preventDefault();
    var form = $("#form")[0];
    var address = form.children[0].value;
    var time = form.children[1].value;
    getLongLatAndGoToAddress(address);
}

function createPolygon(polygonInfo, probability=null) {
//    var color;
//    if (probability > 0.8) {
//        color = "green";
//    } else if (probability >= .4) {
//        color = "goldenrod";
//    } else if (probability < .4) {
//        color = "red";
//    } else {
//        color = "blue";
//    }
    var poly = L.polygon(polygonInfo.coords, {color: "blue"});
    poly.addTo(map);
    $("path")[polygonInfo.index - 1].setAttribute('data-id',polygonInfo.Name);
}

function parseTimestamp(timestamp) {
    time = timestamp.split(":");
    var hour = parseInt(time[0]);
    var minute = parseInt(time[1]);
    var parsedTime = parseFloat(hour + (minute / 60));
    return parsedTime;
}

function changeReportStatus() {
    clearOpacityDiv();
    $("#table").remove();
    var reportButton = $("#report-flag");
    reporting = !reporting;
    var mapElement = $("#map");
    if (reporting) {
        mapElement.css({ cursor: "pointer" });
        reportButton.attr('value', "Stop Reporting").addClass("red").removeClass("green");
    } else {
        mapElement.css({ cursor: "grab" });
        reportButton.attr('value', "Report a Free Space").addClass("green").removeClass("red");
        deleteMapMarkers();
    }
}

function clearOpacityDiv() {
    opacityDiv.remove();
    logo.addClass('smallLogo');
    logo.removeClass('bigLogo');
}

function getTableData(lat, lng) {
    var time = $("input[type='time']").val();
    $.ajax({
        type: "POST",
        url: "/get_parking_spot",
        dataType: 'json',
        contentType: 'application/json',
        data: {
            lat: lat,
            long: lng,
            time: time
        },
        success: function(response) {
            console.log(response);
            addTable(JSON.parse(response));
        }
    })
}

function addTable(tableData) {
    $("#table").remove();
    var table = $('<table/>').attr('id','table');
    $('body').append(table);
    table.addClass('table');
    var header = $('<tr/>');
    var name = $('<th/>').text("Area");
    var prob = $("<th/>").text("Probability");
    var dist = $("<th/>").text("Distance");
    var rank = $("<th/>").text("Rank")
    header.append(name).append(prob).append(dist).append(rank);
    table.append(header);
    for (var i = 0; i < tableData.data.length; i++) {
        var row = $("<tr/>");
        var name = $("<td/>").text(tableData.data[i][0]);
        var prob = $("<td/>").text(tableData.data[i][2].toString().slice(0,4));
        var dist = $("<td/>").text(tableData.data[i][1]);
        var rank = $("<td/>").text(i + 1);
        row.append(name).append(prob).append(dist).append(rank);
        table.append(row);
    }

}

function renderPolygons() {
    $.ajax({
        type: 'GET',
        url: '/get_areas',
        dataType: 'json',
        success: function (resp) {
            window.polygons = resp.polygons;
            for (var i = 0; i < resp.polygons.length; i++) {
                createPolygon(resp.polygons[i]);
            }
        }
    })
}

// Address autocomplete

// placeSearch({
//     key: `${MAPQUEST_API_KEY}`,
//     container: document.querySelector('#search-input'),
//     style: false
//   });


$(document).ready(function () {
    $("#form").submit(submitFunction);
    $("#report-flag").click(changeReportStatus);
    renderPolygons();
});
