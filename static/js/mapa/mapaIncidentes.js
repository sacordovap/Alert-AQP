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
            //  const contentString = '<div class="d-inline-block" style="width: 18rem;"><img class="w-25" style="vertical-align: top;" src="http://127.0.0.1:8000/media/IMG-20211001-WA0003_ovOZOzC.jpg"alt="Card image cap" /><div class="d-inline-block ml-2"><h6>Titulos</h6><p>Descripcion</p><small class="text-muted">4 de Abril 2021 a las 5 pm</small></div></div>';
            // const contentString = '<div class="card m-0 p-0" style="width: 18rem;"><img class="card-img-top mx-auto" src="http://127.0.0.1:8000/media/IMG-20211001-WA0003_ovOZOzC.jpg"alt="Card image cap" style="width: 50px;"><div class="card-body"><h5 class="card-title">Card title</h5><p class="card-text">Some quick example text to build on the card title and make up the bulk of the card\'scontent.</p></div></div>';


            data.forEach(incidente => {
                const latLng = new google.maps.LatLng(incidente.latitud, incidente.longitud);
                let marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                });

                let contentString = htmlContentIncidente(incidente);
                let infowindow = new google.maps.InfoWindow({
                    content: contentString,
                });

                marker.addListener("mouseover", () => {
                    infowindow.open({
                        anchor: marker,
                        map,
                        shouldFocus: false,
                    });
                });
                marker.addListener("mouseout", () => {
                    infowindow.close();
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

    function htmlContentIncidente(incidente) {
        url = incidente.imagen_video;
        fecha_hora = incidente.fecha + " "+incidente.hora;
        let contentString = '<div class="d-inline-block" style="width: 18rem;"><img class="w-25" style="vertical-align: top;" src="'+url+'" alt="Card image cap" /><div class="d-inline-block ml-2"><h6>' + incidente.titulo + '</h6><p>' + incidente.descripcion + '</p><small class="text-muted">'+fecha_hora+'</small></div></div>';
        return contentString;
    }

});
