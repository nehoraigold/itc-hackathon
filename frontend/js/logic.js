var map = L.map('map').setView([32.0853, 34.7818], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'sk.eyJ1IjoibmVob3JhaWdvbGQiLCJhIjoiY2pxZjVmYzh6NGxzODQybGN5bTlwNHBpeiJ9.ruE0eqcqGrt8_hfv3VOGBg'
}).addTo(map);