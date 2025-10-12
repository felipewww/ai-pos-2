<template>
    <div class="card mt-2">
        <div class="card-body position-relative">
            <div class="route-info" v-if="deliveryPoint.hasRoute()" :style="{backgroundColor: deliveryPoint.routeProps.color}">
                Rota {{ deliveryPoint.routeProps.id }}
            </div>
            <div class="row">
                <div class="col d-flex mt-2">
                    <span class="dp-idx position-absolute" @click="viewInMap">{{idx}}</span>
                    <span class="form-check form-switch">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            v-model="deliveryPoint._isPriority"
                        />
                    </span>
                    {{deliveryPoint.address.split('-')[0]}}
                </div>
                <div class="col-12">
<!--                    <span>Prioridade?</span>-->
<!--                    <div class="btn-group" role="group" aria-label="Basic example">-->
<!--                        <button @click="deliveryPoint.setPriority(true)" type="button" :class="cssPriority()">Sim</button>-->
<!--                        <button @click="deliveryPoint.setPriority(false)" type="button" :class="cssNoPriority()">Não</button>-->
<!--                    </div>-->

<!--                    <div class="form-check form-switch">-->
<!--                        <input class="form-check-input" type="checkbox" role="switch" id="switchCheckDefault">-->
<!--                        <label class="form-check-label" for="switchCheckDefault">Default switch checkbox input</label>-->
<!--                    </div>-->
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {DeliveryPoint} from "@/types/delivery-point.ts";

function setp($event) {
    alert($event.target.value);
    // ($event) => deliveryPoint.setPriority($event.target.value)
}

const props = defineProps({
    deliveryPoint: {
        type: Object as () => DeliveryPoint,
        required: true,
    },
    idx: {
        type: Number,
        required: true,
    }
})


function viewInMap() {
    props.deliveryPoint.showMarker()

    setTimeout(() => {
        props.deliveryPoint.removeMarker()
    }, 3000)
}

function cssPriority() {
    const css = ['btn btn-sm']

    if (props.deliveryPoint.isPriority) {
        css.push('btn-success')
    } else {
        css.push('btn-secondary')
    }

    return css;
}

function cssNoPriority() {
    const css = ['btn btn-sm']

    if (!props.deliveryPoint.isPriority) {
        css.push('btn-info')
    } else {
        css.push('btn-secondary')
    }

    return css;
}
</script>

<style scoped>
.route-info {
    top: 0;
    left: 0;
    padding: 0px 5px;
    font-weight: bold;
    font-size: 12px;
    border-radius: 0 0 6px 0;
    position: absolute;
}

.dp-idx {
    top: 0;
    right: 0;
    background: #0d6efd;
    padding: 0px 5px;
    color: #fff;
    font-weight: bold;
    font-size: 13px;
    border-radius: 0 0 0 6px;;
}
</style>
