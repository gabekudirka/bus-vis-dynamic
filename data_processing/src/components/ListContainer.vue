<template>
  <div>
    <i 
        class="fas fa-question-circle helpBtn"  
        @click="showModal"
        title="Help"
    ></i>
    <HelpModal v-show="modalVisible" @close="closeModal"/>
    <ToggleSwitch :initShowBusses="showBusses" /> 
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
import HelpModal from './HelpModal.vue';

export default {
    name: 'ListContainer',
    components: {
        ToggleSwitch,
        // RoutesList,
        StationsList,
        BussesList,
        HelpModal
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
    data() {
        return {
            modalVisible: false
        };
    },
    computed: {
        showBusses: function () {
            return this.$store.state.showBusses;
        }
    },
    methods: {
        showModal() {
            this.modalVisible = true;
        },
        closeModal() {
            this.modalVisible = false;
        },
        toggleView(showBussesVal) {
            // this.$store.dispatch('changeShowBusses', showBussesVal);
        }
    },
};

</script>

<style>
.helpBtn{
    font-size: x-large;
    color: #94cecb;
    position:fixed;
    top: 5px;
    left: 5px;
}
.helpBtn:hover{
    cursor: pointer;
}
#routeList{
    overflow-x: hidden;
    overflow-y: auto;
}
/* div.container {
  max-width: 80%;
} */

</style>
