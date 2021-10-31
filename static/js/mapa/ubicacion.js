$(function () {

    initialize();

    //funcion que elimina la ubicacion
    function eliminarUbicacion(data) {
        console.log(data);
        $('#data').html(data.msg);
        $("#cars").change(eventCambiarPunto);
        $("#deleteUbicacion").click(eventEliminarUbicacion);
    }

    //evento que se ejecuta cuando se elimina una ubicacion
    function eventEliminarUbicacion(e) {

        console.log(e);

        //verificamos que tenga un valor el select
        var value = $('#cars').val()

        console.log(value);

        if (value) {

            $.ajax({

                type: 'POST',
                url: '/app1/coords/eliminar',
                data: { value: value },
                dataType: 'json',
                success: eliminarUbicacion,
                error: function (result) {
                    alert(result);
                }
            });

        }
    }

    //agregamos la funcion al boton
    $("#deleteUbicacion").click(eventEliminarUbicacion);


    //funcion para cambiar la ubicacion
    function cambiarPunto(data) {
        var pos = new google.maps.LatLng(data.lat, data.lng);
        marker.setPosition(pos)
        map.setCenter(pos);
    }

    //evento que se ejecuta cuando se cambia de ubicacion
    function eventCambiarPunto(e) {
        try {
            var element = $(this).find('option:selected');
            var value = element.attr("value");
            console.log(value);
            console.log(e);

            $.ajax({
                //type: 'GET',
                type: 'POST',
                url: '/app1/coords/obtener',
                data: { value: value },
                dataType: 'json',
                success: function (data) {
                    console.log(data);


                    var da = (data.lat != "" && !isNaN(data.lat) && ((data.lat == parseInt(data.lat)) || (data.lat == parseFloat(data.lat))));

                    console.log(da);

                    if (da == true) {
                        cambiarPunto(data);
                    }

                },
                error: function (result) {
                    alert(result);
                }
            });
        }
        catch (error) {
            console.log(error);
        }

    }

    //agregamos la funcion a la lista
    $("#cars").change(eventCambiarPunto);


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
            draggable: true,
            title: "Arrastrame!"
        });

        getMarkerCoords(marker);

        google.maps.event.addListener(marker, 'position_changed', function () {
            getMarkerCoords(marker);
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

    //funcion que se ejecuta cada vez que se guarda un nuevo punto
    $('#form_coords').submit(function (e) {

        e.preventDefault();

        $.post('/app1/coords/save', $(this).serialize(), function (data) {
            if (data.ok) {
                console.log(data.msg);
                $('#data').html(data.msg);
                $("#cars").change(eventCambiarPunto);
                $("#deleteUbicacion").click(eventEliminarUbicacion);
                $('#form_coords').each(function () { this.reset(); });
            }
            else {
                console.log(data.msg);
            }
        }, 'json');

        return false;
    });
});
