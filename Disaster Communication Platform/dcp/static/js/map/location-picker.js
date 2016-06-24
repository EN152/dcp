function newMapScriptPicker(divMapId, valueLocationXId, valueLocationYId) {
    //set the start focus of the map
    var map = L.map(divMapId).setView([37.804146, -122.275045], 15);
    
    //contributors:
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);
    
    
    // Add geocoding plugin etc. search bar
    var options = {
        bounds: true,
        position: "topleft",
        expanded: true
    }
    
    // add search key and options to the map
    var geocoder = L.control.geocoder('search-Hv2UM4h', options).addTo(map);
    
    // when we select a city wich we searched for we are putting that into the 
    geocoder.on('select', function (e) {
        console.log('highlight', e);
        document.getElementById(valueLocationXId).value = e.latlng.lat
        document.getElementById(valueLocationYId).value = e.latlng.lng
    });
    
    // if the map was able to find my current location
    map.on('locationfound', function (e) {
        marker = L.marker([e.latitude, e.longitude], { draggable: false });
        this.addLayer(marker);
        document.getElementById(valueLocationXId).value = e.latitude;
        document.getElementById(valueLocationYId).value = e.longitude;
    });
    
    // start the location tracker
}
function getCurrentLocation() {
    var lc = L.control.locate().addTo(map);
    lc.start();
}