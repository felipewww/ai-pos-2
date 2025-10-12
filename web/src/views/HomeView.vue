<template>
    <div>
        <div v-show="isLoading" id="loading">
            Calculando
        </div>
        <div class="row">
            <div class="col">
                <div v-if="!deliveryPoints.length">
                    Selecione os pontos no mapa para criar um ponto de entrega
                </div>
                <div class="row">
                    <div class="col-12" v-if="routes.length">
                        <div>Selecione as rotas geradas a serem exibidas</div>
                        <div v-for="route of routes" class="btn-group">
                            <div
                                :style="{backgroundColor: (route.showing) ? route.color : 'black', borderColor: route.color, border: `3px solid ${route.color}`}"
                                class="btn btn-dark"
                                @click="showActiveRoutes(route)"
                            >
                                Rota {{route.id}} - {{route.points.length}} pontos
                            </div>
                        </div>
                    </div>

                    <!-- exibir pontos sem rota -->
                    <div v-if="!routes.length" class="col-6 g-2" v-for="(dp, idx) of deliveryPoints">
                        <CDeliveryPoint
                            :idx="idx+1"
                            :delivery-point="dp"/>
                    </div>

                    <!-- exibir cards ordenados por rota criada -->
                    <div v-else class="col-6 g-2" v-for="(route, idx) of routes">
                        <div v-if="route.showing" v-for="(dp, idx) of route.points">
                            <CDeliveryPoint
                                :idx="idx+1"
                                :delivery-point="dp"/>
                        </div>
                    </div>
                </div>
                <div class="card" v-if="gptConversation">
                    <div class="card-body">
                        {{gptConversation}}
                    </div>
                </div>
            </div>
            <div class="col g-2">
                <div class="card">
                    <div class="card-body">
                        <div class="map-container">
                            <br>
                            <div ref="mapEl" class="map"></div>
                            <br>
                            <div class="row" v-if="deliveryPoints.length >= 3">
                                <div></div>
                                <div class="col-12 text-center" v-if="isPriorityDelivery">
                                    <div class="alert alert-info text-center" role="alert">
                                        O total de ( {{prioritiesCount}} ) entregas prioritárias criará ( {{prioritiesCount / 2}} ) rota(s)
                                    </div>
                                </div>
                                <div class="col-12" v-if="!isPriorityDelivery">
                                    <div class="row">
                                        <div class="col-12" v-if="prioritiesCount > 0">
                                            <div class="alert alert-warning text-center" role="alert">
                                                As prioridades não formam duplas e serão distribuidas entre rotas distintas
                                            </div>
                                        </div>
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
                                        <div class="btn btn-danger" @click="hideAll">Limpar mapa</div>
                                        <div class="btn btn-danger" @click="clearRoutes">Deletar Rotas</div>
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
import {randomColorQuadrant2} from "@/utils/utils.ts";

const apiService = new ApiService();

const isLoading = ref(false);
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
let routeRenderers = ref<google.maps.DirectionsRenderer[]>([])

const currentMarkerNumber = computed(() => {
    return (deliveryPoints.value.length + 1).toString()
})

const prioritiesCount = computed(() => {
    let prioritiesCount = 0;
    deliveryPoints.value.map((item, idx) => {
        if (item.isPriority) {
            prioritiesCount++;
        }
    })

    return prioritiesCount;
})

const isPriorityDelivery = computed(() => {
    return prioritiesCount.value % 2 === 0;
})

const deliveryPointsHashmap = computed(() => {
    const map: { [key: string]: number } = {}

    deliveryPoints.value.map((item, idx) => {
        map[item.id] = idx;
    })

    return map;
})

const gptConversation = ref('');

onMounted(async () => {
    apiService.getGmapsKey()
        .then(async (res) => {
            const response = await res.json() as { data: string };
            API_KEY.value = response.data

            await mountMap()
        })
});

function showActiveRoutes(route: RouteCalc) {
    hideAll();

    route.showing = (!route.showing);

    nextTick(() => {
        routes.value.map(r => {
            if (r.showing) {
                traceRouteCluster(r)
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

    map.value = new Map(mapEl.value, {
        center: {
            lat: -23.220512,
            lng: -45.890889,
        }, // SJC
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

function hideRoutes() {
    // routes.value.map(r => {
    //     r.showing = false;
    // })

    routeRenderers.value.forEach(r => r.setMap(null))
    routeRenderers.value = []
    routeMarkers.value.map(m => {
        m.setMap(null)
        m.setOpacity(0)
        m.setVisible(false)
    })
    routeMarkers.value = []
}

function hidePoints() {
    deliveryPoints.value.map(dp => {
        dp.removeMarker()
    })
}

function hideAll() {
    hideRoutes()
    hidePoints()
}

function clearRoutes() {
    routes.value.map(r => {
        r.showing = false;
    })

    deliveryPoints.value.map(dp => {
        dp.unassignRoute()
        dp.showMarker()
    })

    routes.value = []

    gptConversation.value = ''
}

function traceRouteCluster(route: RouteCalc) {
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
                strokeColor: (p.isPriority) ? '#8dff66' : "#FFF",
                strokeWeight: (p.isPriority) ? 4 : 2,
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

    // hideRoutes()
    hideAll();

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

    isLoading.value = true;

    apiService.calculateRoutes(body)
        .then(async (res) => {
            const response = await res.json() as { data: PyResponse };

            gptConversation.value = response.data.conversation;
            routes.value = response.data.routes.map((route, idx) => {
                const color = randomColorQuadrant2()
                const deliveryPointsMapped: DeliveryPoint[] = []

                route.deliveryPoints.map(p => {
                    const idx = deliveryPointsHashmap.value[p.id]
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
        })
        .catch(error => {
            alert('Algo deu errado!')
        })
        .finally(() => {
            isLoading.value = false
        })
}
</script>

<style>
div#loading {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgb(0 0 0 / 90%);
    z-index: 999;
}

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

