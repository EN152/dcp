function initialMap(mapid, location_x, location_y, title) {
    var mymap = L.map(mapid).setView([location_x.replace(",", "."), location_y.replace(",", ".")], 13);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
                        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                            'Imagery © <a href="http://mapbox.com">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mymap);
    L.marker([location_x.replace(",", "."), location_y.replace(",", ".")]).addTo(mymap).bindPopup("<b>" + title +"</b>");
    var popup = L.popup();
}