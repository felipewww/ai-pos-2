<template>
    <div>
        <div class="row">
            <div class="col">
                <div v-if="!deliveryPoints.length">
                    Selecione os pontos no mapa para criar um ponto de entrega
                </div>
                <div class="row">
                    <div class="col-6 g-2" v-for="(dp, idx) of deliveryPoints">
                        <CDeliveryPoint
                            :idx="idx+1"
                            :delivery-point="dp"/>
                    </div>
                </div>
            </div>
            <div class="col g-2">
                <div class="card">
                    <div class="card-body">
                        <div class="map-container">
                            <div v-if="routes.length">
                                <div v-for="route of routes">
                                    <div
                                        class="btn"
                                        :style="{backgroundColor: (route.showing) ? route.color : 'gray'}"
                                        @click="showActiveRoutes(route)"
                                    >
                                        Rota {{route.id}}
                                    </div>
                                </div>
                            </div>
                            <br>
                            <div ref="mapEl" class="map"></div>
                            <br>
                            <div class="row" v-if="deliveryPoints.length >= 3">
                                <div class="col-12">
                                    <div class="row">
                                        <div class="col-6">
                                            <label class="form-label">Mín. de Veículos (até {{vehiclesForm.max}})</label>
                                            <input
                                                v-model="vehiclesForm.min"
                                                :max="(vehiclesForm.max) ? vehiclesForm.max : 1"
                                                min="1"
                                                class="form-control"
                                                type="number"
                                                placeholder="Mín. de veículos"
                                                autocomplete="off"/>
                                        </div>
                                        <div class="col-6">
                                            <label class="form-label">Máx. de Veículos (até {{Math.floor(deliveryPoints.length / 2)}})</label>
                                            <input
                                                v-model="vehiclesForm.max"
                                                :max="Math.floor(deliveryPoints.length / 2)"
                                                min="1"
                                                class="form-control"
                                                type="number"
                                                placeholder="Máx. de veículos"
                                                autocomplete="off"
                                            />
                                        </div>
                                    </div>
                                </div>
                                <div class="col-12 mt-2 d-flex justify-content-center">
                                    <div class="btn-group">
                                        <div class="btn btn-success" @click="calcRoutes">Calcular rotas</div>
                                        <div class="btn btn-danger" @click="clearAll">Limpar mapa</div>
                                    </div>
                                </div>
                            </div>
                            <div v-else>
                                Adicione ao menos 3 pontos de entrega
                            </div>

                            <div v-if="clickedLocation" class="clickedLocation">
                                <p><strong>Endereço:</strong> {{ clickedLocation.address }}</p>
                                <div class="btn btn-success" @click="addMarker">Adicionar Ponto de entrega</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import {computed, nextTick, onMounted, reactive, ref} from "vue";
import { setOptions, importLibrary } from "@googlemaps/js-api-loader";
import {ApiService} from "@/services/api.service.ts";
import {DeliveryPoint} from "@/types/delivery-point.ts";
import CDeliveryPoint from "@/components/c-delivery-point.vue";
import type {DeliveryPointInput} from "@/types/dtos/calculate/delivery-point.input.ts";
import type {PyResponse} from "@/types/dtos/py-response.ts";
import type {CalculateInput} from "@/types/dtos/calculate/calculate.input.ts";
import {RouteCalc} from "@/types/route-calc.ts";

const apiService = new ApiService();

const mapEl = ref<HTMLDivElement>(null);
const clickedLocation = ref<{lat:number; lng:number; address:string}|null>(null);
const API_KEY = ref('')
const map = ref<google.maps.Map>(null);
const currentMarker = ref<google.maps.Marker>(null);
const deliveryPoints = ref<DeliveryPoint[]>([]);
const routeMarkers = ref<google.maps.Marker[]>([])
const vehiclesForm = reactive({
    min: null,
    max: null,
})

const routes = ref<RouteCalc[]>([])

const currentMarkerNumber = computed(() => {
    return (deliveryPoints.value.length + 1).toString()
})

const deliveryPointsHashmap = computed(() => {
    const map: { [key: string]: number } = {}

    deliveryPoints.value.map((item, idx) => {
        map[item.id] = idx;
    })

    return map;
})

onMounted(async () => {
    apiService.getGmapsKey()
        .then(async (res) => {
            const response = await res.json() as { data: string };
            API_KEY.value = response.data

            await mountMap()
        })
});

function showActiveRoutes(route: RouteCalc) {
    clearAll();

    route.showing = (!route.showing);

    nextTick(() => {
        routes.value.map(r => {
            if (r.showing) {
                console.log(`should SHOW route ${r.id}`)
                traceRouteCluster(r)
            } else {
                console.log(`should NOT show route ${r.id}`)
            }
        })
    })
}

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
    currentMarker.value.setMap(null);
}

// Lista global para armazenar renderizadores ativos (para poder limpar depois)
let routeRenderers = ref<google.maps.DirectionsRenderer[]>([])

function clearRoutes() {
    // usedColors.clear();
    routeRenderers.value.forEach(r => r.setMap(null))
    routeRenderers.value = []
    routeMarkers.value.map(m => {
        m.setMap(null)
        m.setOpacity(0)
        m.setVisible(false)
    })
    routeMarkers.value = []
}

function clearPoints() {
    deliveryPoints.value.map(dp => {
        dp.removeMarker()
    })
}

function clearAll() {
    clearRoutes()
    clearPoints()
}

// const usedColors = new Set<string>()

// function traceMultipleRoutes(allClusters: DP[][]) {
//     // Remove rotas antigas
//     clearRoutes()
//
//     // Paleta de cores (pode aumentar conforme número de clusters)
//     // const colors = [
//     //     "#FF0000",
//     //     "#008000",
//     //     "#0000FF",
//     //     "#FFA500",
//     //     "#800080",
//     //     "#00CED1",
//     //     "#d10088",
//     //     "#ffe145",
//     //     "#370000",
//     //     "#000000",
//     //     "#ffa86e",
//     // ]
//
//     // const availableColors = colors.filter(c => !usedColors.has(c))
//
//     allClusters.forEach((dps, idx) => {
//         // const randomIndex = Math.floor(Math.random() * availableColors.length)
//         // const color = colors[randomIndex]
//         // usedColors.add(color)
//         traceRouteCluster(dps, color)
//     })
// }

function traceRouteCluster(route: RouteCalc) {
    // if (!dps || dps.length < 2) return
    // if (route.showing) {
    //     return;
    // }

    // route.showing = true;

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map.value,
        suppressMarkers: true, // desativa marcadores padrão
        preserveViewport: true, // evita o mapa resetar o zoom a cada rota
        polylineOptions: {
            strokeColor: route.color,
            strokeWeight: 5,
            strokeOpacity: 0.8,
        },
    })

    const origin = route.points[0]
    const destination = route.points[route.points.length - 1]
    const waypoints = route.points.slice(1, -1).map((r) => ({ location: { lat: r.lat, lng: r.lng } }))

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
                routeRenderers.value.push(directionsRenderer)
                addCustomMarkers(route.points, route.color)
            } else {
                console.error("Erro ao calcular rota:", status)
            }
        }
    )
}

function addCustomMarkers(dps: DeliveryPoint[], color: string) {
    dps.forEach((p, i) => {
        const routeMarker = new google.maps.Marker({
            position: { lat: p.lat, lng: p.lng },
            map: map.value,
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

        routeMarkers.value.push(routeMarker)
    })
}

function calcRoutes() {
    if (deliveryPoints.value.length < 3) {
        alert('Necessário ao menos 3 pontos')
        return;
    }

    const deliveryPointsInput: DeliveryPointInput[] = deliveryPoints.value
        .map(d => ({
            id: d.id,
            address: d.address,
            lat: d.lat,
            lng: d.lng,
            isPriority: d.isPriority,
        }));

    const body: CalculateInput = {
        deliveryPoints: deliveryPointsInput,
        vehicles: vehiclesForm
    }

    apiService.calculateRoutes(body)
        .then(async (res) => {
            const response = await res.json() as { data: PyResponse };

            const colors = [
                "#FF0000",
                "#008000",
                "#0000FF",
                "#FFA500",
                "#800080",
                "#00CED1",
                "#d10088",
                "#ffe145",
                "#370000",
                "#000000",
                "#ffa86e",
            ]

            const usedColors = new Set<string>()

            routes.value = response.data.map((route, idx) => {
                const availableColors = colors.filter(c => !usedColors.has(c))
                const randomIndex = Math.floor(Math.random() * availableColors.length)
                const color = colors[randomIndex]
                usedColors.add(color)

                const deliveryPointsMapped: DeliveryPoint[] = []
                console.log(deliveryPointsHashmap.value)
                route.deliveryPoints.map(p => {
                    console.log(`\nfinding DP by id ${p.id}`)
                    const idx = deliveryPointsHashmap.value[p.id]
                    console.log(`idx found: ${idx}`)
                    const dp = deliveryPoints.value[idx];
                    if (!dp) {
                        alert("No deliveryPoints found");
                    } else {
                        deliveryPointsMapped.push(dp);
                    }
                })

                const routeCalc = new RouteCalc(
                    idx,
                    color,
                )

                deliveryPointsMapped.map(d => {
                    routeCalc.addDeliveryPoint(d)
                })

                return routeCalc
            })

            deliveryPoints.value.map((p, i) => {
                p.removeMarker()
            })

            console.log('routes.value:::')
            console.log(routes.value)

            // traceMultipleRoutes(toRoutes);
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
    width: 100%;
    height: 700px;
}

.map {
    width: 100%;
    height: 500px;
}

.clickedLocation {
    margin-top: 10px;
    padding: 10px;
    width: 90%;
    border-radius: 6px;
}
</style>

