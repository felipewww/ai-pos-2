<template>
    <div class="card">
        <div class="card-body">
            <div v-if="deliveryPoint.hasRoute()" :style="{backgroundColor: deliveryPoint.routeProps.color}">
                Rota {{ deliveryPoint.routeProps.id }}
            </div>
            <div class="row">
                <div class="col">
                    <span @click="viewInMap">{{idx}}</span> - {{deliveryPoint.address.split('-')[0]}}
                </div>
                <div class="col">
                    <div>Prioridade?</div>
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <button @click="deliveryPoint.setPriority(true)" type="button" :class="cssPriority()">Sim</button>
                        <button @click="deliveryPoint.setPriority(false)" type="button" :class="cssNoPriority()">Não</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {DeliveryPoint} from "@/types/delivery-point.ts";

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

</style>
