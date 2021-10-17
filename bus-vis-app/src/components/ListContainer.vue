<template>
  <div>
    <ToggleSwitch :initShowBusses="showBusses" @toggleView="toggleView"/> 
    <div class="lists">
        <!-- <RoutesList v-if="showBusses"/> -->
        <BussesList v-if="showBusses" :planObj="planBusses"/>
        <StationsList v-if="!showBusses" :planObj="planObj"/>
    </div>
  </div>
</template>

<script>
import ToggleSwitch from './ToggleSwitch.vue';
// import RoutesList from './RoutesList.vue';
import StationsList from './StationsList.vue';
import BussesList from './BussesList.vue';

export default {
    name: 'ListContainer',
    components: {
        ToggleSwitch,
        // RoutesList,
        StationsList,
        BussesList
    },
    props: {
        planObj: {
            type: Object,
            required: true,
        },
        planBusses: {
            type: Object,
            required: true
        }
    },
    computed: {
        showBusses: function () {
            return this.$store.state.showBusses;
        }
    },
    methods: {
        toggleView(showBussesVal) {
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
