<template>
    <div>
        <div class="row">
            <div class="col">
                <div v-if="!deliveryPoints.length">
                    Selecione os pontos no mapa para criar um ponto de entrega
                </div>
                <div v-else>
                    Pontos de Entrega
                </div>
                <CDeliveryPoint
                    v-for="(dp, idx) of deliveryPoints"
                    :idx="idx+1"
                    :delivery-point="dp"/>
            </div>
            <div class="col">
                <div class="map-container">
                    <div ref="mapEl" class="map"></div>
                    <div class="btn btn-success" @click="calcRoutes">Calcular rotas</div>
                    <div v-if="clickedLocation" class="clickedLocation">
                        <p><strong>Endereço:</strong> {{ clickedLocation.address }}</p>
                        <div class="btn btn-success" @click="addMarker">Adicionar Ponto de entrega</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {computed, nextTick, onMounted, ref} from "vue";
import { setOptions, importLibrary } from "@googlemaps/js-api-loader";
import AdvancedMarkerElement = google.maps.marker.AdvancedMarkerElement;
import {ApiService} from "@/services/api.service.ts";
import {DeliveryPoint} from "@/types/delivery-point.ts";
import CDeliveryPoint from "@/components/c-delivery-point.vue";
import type {DeliveryPointInput} from "@/types/dtos/delivery-point.input.ts";
import type {PyResponse} from "@/types/dtos/py-response.ts";

const mapEl = ref<HTMLDivElement>(null);
const clickedLocation = ref<{lat:number; lng:number; address:string}|null>(null);

const API_KEY = ref('')

const apiService = new ApiService();

const mapRef = ref(null);

const map = ref<google.maps.Map>(null);
const currentMarker = ref<google.maps.Marker>(null);
// const markers = ref<google.maps.Marker[]>([]);

const currentMarkerNumber = computed(() => {
    // return (markers.value.length + 1).toString()
    return (deliveryPoints.value.length + 1).toString()
})

const deliveryPoints = ref<DeliveryPoint[]>([]);

onMounted(async () => {
    apiService.getGmapsKey()
        .then(async (res) => {
            const response = await res.json() as { data: string };
            API_KEY.value = response.data

            await mountMap()
        })
});

async function mountMap() {

    setOptions({ key: API_KEY.value, v: "weekly" });

    // Carregue libs necessárias
    const { Map }     = await importLibrary("maps");
    const { Marker }  = await importLibrary("marker");
    const { Geocoder }= await importLibrary("geocoding");
    const { AdvancedMarkerElement }= await importLibrary("marker");

    map.value = new Map(mapEl.value, {
        center: {
            lat: -23.220512,
            lng: -45.890889,
            // lat: -23.499191,
            // lng: -46.625594,
        }, // SP
        zoom: 14,
        styles: [
            {
                featureType: "poi",
                stylers: [{ visibility: "off" }],
            },
            {
                featureType: "transit",
                elementType: "labels.icon",
                stylers: [{ visibility: "off" }],
            },
        ],
    });
    //
    // let marker: google.maps.Marker | null = null;
    // let marker: AdvancedMarkerElement = null;
    const geocoder = new Geocoder();

    map.value.addListener("click", async (e: google.maps.MapMouseEvent) => {
        const ll = e.latLng; if (!ll) return;
        const lat = ll.lat(), lng = ll.lng();

        const res = await geocoder.geocode({ location: { lat, lng } });
        const address = res.results?.[0]?.formatted_address ?? "Endereço não encontrado";
        clickedLocation.value = { lat, lng, address };

        if (currentMarker.value) {
            currentMarker.value.setPosition({lat, lng,})
            return;
        }

        currentMarker.value = new google.maps.Marker({
            position: { lat, lng },
            map: map.value,
            label: {
                text: currentMarkerNumber.value,
                color: "white",
                fontSize: "14px",
                fontWeight: "bold",
            },
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: "red",
                fillOpacity: 1,
                strokeWeight: 1,
                scale: 10,
            }
        });
    });
}

function addMarker() {
    const marker = new google.maps.Marker({
        position: {
            lat: clickedLocation.value.lat,
            lng: clickedLocation.value.lng,
        },
        map: map.value,
        label: {
            text: currentMarkerNumber.value,
            color: "white",
            fontSize: "14px",
            fontWeight: "bold",
        },
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: "blue",
            fillOpacity: 1,
            strokeWeight: 1,
            scale: 10,
        }
    });

    deliveryPoints.value.push(
        new DeliveryPoint(
            clickedLocation.value.address,
            clickedLocation.value.lat,
            clickedLocation.value.lng,
            marker,
        )
    )

    clickedLocation.value = null;

    currentMarker.value = null;

    // const dpsPriority = [
    //     {
    //         "lat": -23.245886,
    //         "lng": -45.899743,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.245046,
    //         "lng": -45.89709,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.246538,
    //         "lng": -45.89606,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.248786,
    //         "lng": -45.893156,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.245235,
    //         "lng": -45.89247,
    //         "is_priority": true
    //     },
    //     {
    //         "lat": -23.242545,
    //         "lng": -45.893361,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.243112,
    //         "lng": -45.8959,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.24057,
    //         "lng": -45.899422,
    //         "is_priority": true
    //     },
    //     {
    //         "lat": -23.24057,
    //         "lng": -45.900794,
    //         "is_priority": true
    //     },
    //     {
    //         "lat": -23.242839,
    //         "lng": -45.902075,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.248008,
    //         "lng": -45.904042,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.24679,
    //         "lng": -45.900543,
    //         "is_priority": true
    //     }
    // ]

    // const dpsNoPrio = [
    //     {
    //         "lat": -23.225839,
    //         "lng": -45.89416,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.227301,
    //         "lng": -45.891361,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.225819,
    //         "lng": -45.888817,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.225325,
    //         "lng": -45.886689,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.222092,
    //         "lng": -45.88547,
    //         "is_priority": true
    //     },
    //     {
    //         "lat": -23.221202,
    //         "lng": -45.891324,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.220456,
    //         "lng": -45.893967,
    //         "is_priority": false
    //     },
    //     {
    //         "lat": -23.221031,
    //         "lng": -45.895959,
    //         "is_priority": false
    //     }
    // ]

    // traceMultipleRoutes([
    //     dpsPriority,
    //     dpsNoPrio
    // ])
}

type DP = {
    lat:number,
    lng:number,
}

// Lista global para armazenar renderizadores ativos (para poder limpar depois)
const routeRenderers: google.maps.DirectionsRenderer[] = []

function traceMultipleRoutes(allClusters: DP[][]) {
    // Remove rotas antigas
    routeRenderers.forEach(r => r.setMap(null))
    routeRenderers.length = 0

    // Paleta de cores (pode aumentar conforme número de clusters)
    const colors = ["#FF0000", "#008000", "#0000FF", "#FFA500", "#800080", "#00CED1"]

    allClusters.forEach((dps, idx) => {
        traceRouteCluster(dps, colors[idx % colors.length])
    })
}

function traceRouteCluster(dps: DP[], color: string) {
    if (!dps || dps.length < 2) return

    const directionsService = new google.maps.DirectionsService()
    const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map.value,
        suppressMarkers: true, // desativa marcadores padrão
        preserveViewport: true, // evita o mapa resetar o zoom a cada rota
        polylineOptions: {
            strokeColor: color,
            strokeWeight: 5,
            strokeOpacity: 0.8,
        },
    })

    const origin = dps[0]
    const destination = dps[dps.length - 1]
    const waypoints = dps.slice(1, -1).map((r) => ({ location: { lat: r.lat, lng: r.lng } }))

    directionsService.route(
        {
            origin,
            destination,
            waypoints,
            travelMode: google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
            if (status === "OK" && result) {
                directionsRenderer.setDirections(result)
                routeRenderers.push(directionsRenderer)

                // Marcadores personalizados
                addCustomMarkers(dps, color)
            } else {
                console.error("Erro ao calcular rota:", status)
            }
        }
    )
}

function addCustomMarkers(dps: DP[], color: string) {
    dps.forEach((p, i) => {
        new google.maps.Marker({
            position: { lat: p.lat, lng: p.lng },
            map: map.value,
            // label: `${i + 1}`, // apenas texto, sem objeto
            label: {
                text: String(i + 1),
                color: "#FFF",
                fontSize: "12px",
                fontWeight: "bold",
            },
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 16,
                fillColor: color,
                fillOpacity: 1,
                strokeColor: "#FFF",
                strokeWeight: 2,
            },
            // title: p.title,
        })
    })
}

function calcRoutes() {
    if (deliveryPoints.value.length < 3) {
        alert('Necessário ao menos 3 pontos')
        return;
    }

    const deliveryPointsInput: DeliveryPointInput[] = deliveryPoints.value
        .map(d => ({
            address: d.address,
            lat: d.lat,
            lng: d.lng,
            isPriority: d.isPriority,
        }));

    apiService.calculateRoutes(deliveryPointsInput)
        .then(async (res) => {
            const response = await res.json() as { data: PyResponse };

            const toRoutes: DP[][] = response.data.map(route => {
                return route.deliveryPoints.map(p => {
                    return {
                        lat: p.lat,
                        lng: p.lng,
                    }
                })
            })

            traceMultipleRoutes(toRoutes);
        })
        .catch(error => {
            alert('Algo deu errado!')
        })
}
</script>

<style>
.map-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    /*width: 100%;          !* garante largura *!*/
    /*height: 100%;         !* garante altura *!*/
    /*min-height: 500px;    !* previne colapso *!*/
    width: 100%;
    height: 700px;
}

.map {
    width: 100%;          /* 100% da largura do container */
    height: 500px;        /* altura fixa ou pode ser flexível */
}

.clickedLocation {
    margin-top: 10px;
    /*background: #f5f5f5;*/
    padding: 10px;
    width: 90%;
    border-radius: 6px;
}
</style>

