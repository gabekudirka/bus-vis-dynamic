<template>
  <div>
    <ToggleSwitch :initShowBusses="showBusses" @toggleView="toggleView"/> 
    <div class="lists">
        <RoutesList v-if="showBusses"/>
        <StationsList v-if="!showBusses"/>
    </div>
  </div>
</template>

<script>
import ToggleSwitch from './ToggleSwitch.vue';
import RoutesList from './RoutesList.vue';
import StationsList from './StationsList.vue';

export default {
    name: 'ListContainer',
    components: {
        ToggleSwitch,
        RoutesList,
        StationsList
    },
    computed: {
        showBusses: function () {
            return this.$store.state.showBusses;
        }
    },
    methods: {
        updateMap(val) {
            console.log('update map', val);
        },
        selectedMethod(val) {
            console.log('selected method', val);
        },
        toggleView(showBussesVal) {
            console.log('toggle view', showBussesVal);
            this.$store.dispatch('changeShowBusses', showBussesVal);
        }
    },
};

</script>

<style>
#routeList{
    overflow-x: hidden;
    overflow-y: auto;
}
/* div.container {
  max-width: 80%;
} */

</style>
