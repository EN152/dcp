function initialMap(mapid, location_x, location_y, title, radius) {
    var mymap = L.map(mapid).setView([location_x.replace(",", "."), location_y.replace(",", ".")], 13);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(mymap);
    var marker = L.marker([location_x.replace(",", "."), location_y.replace(",", ".")]).addTo(mymap).bindPopup("<b>" + title +"</b>");
    L.circle(marker.getLatLng(), (radius.replace(",", ".") * 1000), {
        fillOpacity: 0.5,
        clickable: false
    }).addTo(mymap);
}