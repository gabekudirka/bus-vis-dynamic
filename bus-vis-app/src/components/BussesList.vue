/* eslint-disable no-confusing-arrow */
<template>
  <div>
    <ul id="busList">
        <li v-for="item in planBusses" 
            :key="item.id"
            :class="[item.id == selectedBus ? 'selected' : '', 'listItem']"
            @click="selectItem(item.id)"
        >
            <i :class="[item.converted? '' : 'hidden', 'fas fa-plug']"></i>
            {{ item.id }}
        </li>
    </ul>
  </div>
</template>

<script>
// import stopsList from '../data/allStops.json';
import p20 from '../data/buses/p20.json';
import p60 from '../data/buses/p60.json';
import p180 from '../data/buses/p180.json';

export default {
    name: 'BussesList',
    props: {
        planObj: {
            type: Object,
            required: true
        }
    },
    computed: {
        plan: function () {
            return this.$store.state.plan;
        },
        selectedBus: function () {
            return this.$store.state.selectedBus;
        },
        planBusses: function () {
            const bs = this.planObj;
            return bs.buses.sort((a, b) => (a.id > b.id) ? 1 : -1);
            // let bs = p180.buses;
            // if (this.plan === 'p20') {
            //     bs = p20.buses;
            // } else if (this.plan === 'p60') {
            //     bs = p60.buses;
            // }
            // return bs.sort((a, b) => (a.id > b.id) ? 1 : -1);            
        },
    },
    methods: {
        selectItem: function (busId) {
            this.$store.dispatch('changeBus', busId);
        }
    }
};

</script>

<style>
.selected {
    color: white;
    background: lightseagreen !important;
}
ul#busList > li:nth-of-type(odd) {
    background-color: white;
}
.listItem{
    padding: 0.6em;
    text-align:left;
}
.hidden{
    visibility: hidden;
}

</style>
