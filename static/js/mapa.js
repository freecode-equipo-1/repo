mapboxgl.accessToken = '{{ mapbox_api_key }}';
var map = new mapboxgl.Map({
    container: 'mapa',
    center: [-66.9036, 10.4806],
    zoom: 12.5,
    style: 'mapbox://styles/mapbox/streets-v11'
});

map.on('load', () => {
    map.addSource('places', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': [
                {% for reporte in reportes %}
                    {
                        'type': 'Feature',
                        'properties': {
                            'description':
                            '<strong>{{ reporte.insumo.nombre }}</strong><p>Costo de {{ reporte.costo }}</p>',
                            'icon': 'information-15'
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [
                                {{ reporte.longitud }},
                                {{ reporte.latitud }}
                            ]
                        }
                    },
                {% endfor %}
            ]
        }
    });
    map.addLayer({
        'id': 'places',
        'type': 'symbol',
        'source': 'places',
        'layout': {
            'icon-image': '{icon}',
            'icon-allow-overlap': true
        }
    });

    // Abrir pop=up (ejemplo tomado de la página de Mapbox)
    map.on('click', 'places', (e) => {
        // Copy coordinates array.
        const coordinates = e.features[0].geometry.coordinates.slice();
        const description = e.features[0].properties.description;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(description)
        .addTo(map);
    });

    // Cursores al entrar y salir de la capa de íconos
    map.on('mouseenter', 'places', () => {
        map.getCanvas().style.cursor = 'pointer';
    });
    map.on('mouseleave', 'places', () => {
        map.getCanvas().style.cursor = '';
    });

    // Permitir al usuario centrar el mapa en su cercanía
    map.addControl(
        new mapboxgl.GeolocateControl({
            positionOptions: {
                enableHighAccuracy: true
            },
            trackUserLocation: true,
            showUserHeading: true
        })
    );
});