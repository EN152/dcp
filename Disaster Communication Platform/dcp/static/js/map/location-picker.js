var map;
var marker;
var circle;
var valueLocationXId;
var valueLocationYId;
var radius = 0;
var staticMarkers = [];
var staticCircles = [];
var redIcon;

function newMapScriptPicker(divMapId, valueLocationXId, valueLocationYId) {
    //set the start focus of the map
    this.map = L.map(divMapId).setView([51.508, -0.11], 13);
    this.valueLocationXId = valueLocationXId;
    this.valueLocationYId = valueLocationYId;
    
    //contributors:
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    map.on('click', eventToMapCreateMaker);
    
    // Add geocoding plugin etc. search bar
    var options = {
        bounds: true,
        position: "topleft",
        expanded: true,
        markers: false
    }
    
    // add search key and options to the map
    var geocoder = L.control.geocoder('search-Hv2UM4h', options).addTo(map);
    // when we select a city wich we searched for we are putting that into the 
    geocoder.on('select', eventToMapCreateMaker);
    
    map.on('locationfound', eventToMapCreateMaker);

    // Create Red Icon
    var RedIcon = L.Icon.Default.extend({
        options: {
            iconUrl: '/static/leafletjs/marker-icon-red.png'
        }
    });
    this.redIcon = new RedIcon();
}
// Fuktionen für den Neuerstellungsmaker
function eventToMapCreateMaker(e) {
    changeMapCreateMarker(e.latlng);
}
function getCurrentLocation() {
    map.locate({
        setView: true});
}
function changeMapCreateMarker(latlng) {
    if (marker != undefined) {
        map.removeLayer(marker)
    }
    marker = L.marker(latlng, { draggable: true });
    map.addLayer(marker);
    changeValuesMapCreate(latlng);
    changeCircleCreateNew();
    marker.on('dragend', function (e) {
        changeValuesMapCreate(marker.getLatLng());
        changeCircleCreateNew();
    });
    marker.on('drag', function (e) {
        changeCircleCreateNew();
    })
}
function changeValuesMapCreate(latlng) {
    document.getElementById(valueLocationXId).value = latlng.lat;
    document.getElementById(valueLocationYId).value = latlng.lng;
}
function newMapCreateRender() {
    map.invalidateSize();
}
function changeCircleCreateNew() {
    if (this.circle != undefined) {
        map.removeLayer(circle);
    }

    this.circle = L.circle(marker.getLatLng(), radius, {
        fillOpacity: 0.5,
        clickable: false
    }).addTo(map);
}
function changeRadiusOnMap(radius) {
    this.radius = 1000 * radius;
    changeCircleCreateNew();
}
// Ende der Funktionen für den Neuerstellungsmarker

// Anfang für statische Elemente
function addToStaticMarkers(location_x, location_y, title) {
    staticMarkers.push((L.marker([location_x.replace(",", "."), location_y.replace(",", ".")], {
        draggable: false,
        icon : redIcon
    })).bindPopup(title));
}
function addToStaticCircles(location_x, location_y, radius, title) {
    staticCircles.push((L.circle([location_x.replace(",", "."), location_y.replace(",", ".")], (radius.replace(",", ".") * 1000), {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.2,
        clickable: true
    })).bindPopup(title));
}
function showStaticMarkers() {
    staticMarkers.forEach(function(entry) {
        map.addLayer(entry);
    });
}
function showStaticCircles() {
    staticCircles.forEach(function(entry) {
        map.addLayer(entry);
    });
}
function hideStaticMarkers() {
    staticMarkers.forEach(function (entry) {
        map.removeLayer(entry);
    });
}
function hideStaticCircles() {
    staticCircles.forEach(function (entry) {
        map.removeLayer(entry);
    });
}
// Anfang für den statischen Marker
function addStaticMarker(location_x, location_y, title) {
    var staticMarker = (L.marker([location_x.replace(",", "."), location_y.replace(",", ".")], {
        draggable: false,
        icon: redIcon
    })).bindPopup(title)
    map.addLayer(staticMarker);
}
function addStaticCircle(location_x, location_y, radius, title) {
    var staticCircle = (L.circle([location_x.replace(",", "."), location_y.replace(",", ".")], (radius.replace(",", ".") * 1000), {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.2,
        clickable: false
    })).bindPopup("<br><b>" + title + "</br>Radius: </b>" + radius + " km")
    map.addLayer(staticCircle);
}