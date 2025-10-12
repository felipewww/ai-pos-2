<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container">
            Postech LogAI
        </div>
    </nav>
    <div class="container-fluid mt-3">
        <div class="container">
            <RouterView />
        </div>
    </div>
</template>

<style scoped>

</style>
