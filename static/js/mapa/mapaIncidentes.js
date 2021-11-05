$(function () {

    initialize();

    function initialize() {
        //mostramos la variable navigator
        console.log(navigator.geolocation);

        if (!(navigator.geolocation == 'undefined')) {
            //verificamos que tenga soporte
            console.log('Geolocation supported');
            try {
                navigator.geolocation.getCurrentPosition(displayLocation, displayError, {
                    timeout: 10000
                });

            }
            catch (error) {
                console.log(error);
            }
        }
        else {
            //una console.loga indicando que no tiene soporte
            console.log('Geolocation unsupported');
        }
    }

    function displayLocation(position) {
        try {
            var cords = position.coords;
            console.log("displayLocation, lat='" + cords.latitude + "'; long='" + cords.longitude + "'");

            lat = cords.latitude
            lng = cords.longitude

            createMap(lat, lng)
        }
        catch (error) {
            console.log(error);
        }
    }


    function displayError(error) {
        var errorstr = "Really unknown error";

        switch (error.code) {
            case error.PERMISSION_DENIED:
                errorstr = "Permission deined";
                break;
            case error.POSITION_UNAVAILABLE:
                errorstr = "Permission unavailable";
                break;
            case error.TIMEOUT:
                errorstr = "Timeout";
                break;
            case error.UNKNOWN_ERROR:
                error = "Unknown error";
                break;
        }

        console.log("GPS error: " + error + " - Message: " + errorstr);

        createMap(13.30272, -87.194107);
    }

    var marker;

    function createMap(lat, lng) {
        console.log(lat);
        console.log(lng);

        var latlng = new google.maps.LatLng(lat, lng);
        var infoWindow = new google.maps.InfoWindow();
        var mapSettings = {
            center: latlng,
            zoom: 15,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }

        map = new google.maps.Map($('#mapa').get(0), mapSettings);


        //var marker = new google.maps.Marker({
        marker = new google.maps.Marker({
            position: latlng,
            map: map,
            draggable: false,
            title: "Arrastrame!"
        });

        getMarkerCoords(marker);


        $.get("/incidentes", {}, (data) => {
           
           data.forEach(incidente => {
            const latLng = new google.maps.LatLng(incidente.latitud, incidente.longitud);
            new google.maps.Marker({
                position: latLng,
                map: map,
            });
           });
           
        });


        //creamos un boton en el medio del mapa
        var geolocationDiv = document.createElement('div');
        var geolocationControl = new GeolocationControl(geolocationDiv, map);

        map.controls[google.maps.ControlPosition.TOP_CENTER].push(geolocationDiv);

    }

    //funcion para crear el boton que muestra la posicion actual dentro del mapa
    function GeolocationControl(controlDiv, map) {

        // Set CSS for the control button
        var controlUI = document.createElement('button');

        controlUI.style.backgroundColor = '#fff';

        controlUI.style.borderStyle = 'solid';
        controlUI.style.borderWidth = '1px';
        controlUI.style.borderColor = 'white';
        controlUI.style.borderRadius = '2px';

        controlUI.style.boxShadow = '0 1px 4px rgba(0,0,0,0.3)';

        controlUI.style.outline = 'none';

        controlUI.style.height = '28px';
        controlUI.style.width = '28px';

        controlUI.style.marginRight = '10px';
        controlUI.style.marginTop = '5px';
        controlUI.style.padding = '0';

        controlUI.style.cursor = 'pointer';

        controlUI.style.textAlign = 'center';

        controlUI.title = 'Click to center map on your location';

        controlDiv.appendChild(controlUI);


        var controlText = document.createElement('div');

        controlText.style.fontFamily = 'Arial,sans-serif';
        controlText.style.fontSize = '10px';

        controlText.style.height = '18px';
        controlText.style.width = '18px';

        controlText.style.margin = '5px';

        controlText.style.backgroundImage = 'url(https://maps.gstatic.com/tactile/mylocation/mylocation-sprite-1x.png)';
        controlText.style.backgroundSize = '180px 18px';
        controlText.style.backgroundPosition = '0 0';
        controlText.style.backgroundRepeat = 'no-repeat';

        controlText.id = 'you_location_img';

        controlUI.appendChild(controlText);

        // Setup the click event listeners to geolocate user
        google.maps.event.addDomListener(controlUI, 'click', geolocate);
    }

    //funcion para marcar la posicion actual
    function geolocate() {
        console.log("Marcar la posicion actual")

        if (navigator.geolocation) {

            navigator.geolocation.getCurrentPosition(function (position) {

                var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

                marker.setPosition(pos)
                map.setCenter(pos);
            });
        }
    }

    //funcion para marcar las coordenadas
    function getMarkerCoords(marker) {
        var markerCoords = marker.getPosition();
        $('#id_lat').val(markerCoords.lat());
        $('#id_lng').val(markerCoords.lng());
        console.log(markerCoords.lat() + '  ' + markerCoords.lng())
    }


});
