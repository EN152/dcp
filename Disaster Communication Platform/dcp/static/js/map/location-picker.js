var map;
var marker;
var circle;
var valueLocationXId;
var valueLocationYId;
var radius = 0;

function newMapScriptPicker(divMapId, valueLocationXId, valueLocationYId) {
    //set the start focus of the map
    this.map = L.map(divMapId).setView([51.508, -0.11], 13);
    this.valueLocationXId = valueLocationXId;
    this.valueLocationYId = valueLocationYId;
    
    //contributors:
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);
    map.on
    
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
    geocoder.on('select', function (e) {
        changeMapCreateMarker(e.latlng);
    });
    
    // if the map was able to find my current location
    map.on('locationfound', function (e) {

        changeMapCreateMarker(e.latlng);
    });
    
    // start the location tracker
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
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.3,
        clickable: false
    }).addTo(map);
}
function changeRadiusOnMap(radius) {
    this.radius = 1000 * radius;
    changeCircleCreateNew();
}