/* eslint-disable max-len */
<template>
  <div class="container-fluid bottom-panel-box">
    <div class="row">
      <div class="col-5 left-align">
          <p class="bus-header"> <b> Bus ID: {{ bus.id }} </b> </p>
          <p> Bus Line: {{ bus.line }} </p>
          <p> Converted: {{ bus.converted }} </p>
          <p> Bus Status: On Route </p>
          <p> Last Stop: {{ bus.stops[0].stop_name }} </p>
          <p> Bus Environmental Impact: {{ bus.environmental_equity }} </p>
      </div>
      <div class="col">
         <p> <b> Charge level over time </b> </p>
      </div>
      <div class="col"><b> Electricity usage </b></div>
    </div>
  </div>
</template>

<script>
import p20 from '../data/buses/p20.json';
import p60 from '../data/buses/p60.json';
import p180 from '../data/buses/p180.json';

export default {
    name: 'BusPanel',
    data() {
        return {
            p20,
            p60,
            p180,
        };
    },
    computed: {
        busId: function () {
            return this.$store.state.selectedBus;
        },
        plan: function () {
            return this.$store.state.plan;
        },
        bus: function () {
            switch (this.plan) {
                case 'p20':
                    return this.p20Dict[this.busId];
                case 'p60':
                    return this.p60Dict[this.busId];
                case 'p180':
                    return this.p180Dict[this.busId];
                default:
                    return this.p20Dict[this.busId];
            }
        },
        p20Dict: function () {
            return this.jsonToDict(p20);
        },
        p60Dict: function () {
            return this.jsonToDict(p60);
        },
        p180Dict: function () {
            return this.jsonToDict(p180);
        },
        
    },
    methods: {
        jsonToDict(jsonData) {
            const buses = {};
            const busData = jsonData;
            for (let i = 0; i < busData.buses.length; i++) {
                const bus = busData.buses[i];
                buses[bus.id] = bus;
            }
            return buses;
        }
    }
};

</script>

<style>
.left-align{
    text-align: left;
    padding-left:1em;
}
p{
    margin-bottom:0.5em !important;
}
</style>
