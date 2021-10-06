/* eslint-disable max-len */
<template>
  <div class="container bottom-panel-box">
    <div class="row absolute">
      <div class="col-5 border">
        <div class="row border">
            Bus ID: {{ bus.id }}
        </div>
        <div class="row">
          <p> Bus Line: {{ bus.line }} </p>
        </div>
        <div class="row">
          <p> Bus Status: On Route </p>
        </div>
        <div class="row">
          <p> Last Stop: {{ bus.stops[0].stop_name }} </p>
        </div>
        <div class="row">
          <p> Bus Environmental Impact: {{ bus.environmental_equity }} </p>
        </div>
      </div>
      <div class="col border">Charge level over time</div>
      <div class="col border">Electricity usage</div>
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
        bus: function () {
            switch (this.$store.state.plan) {
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
div.container {
  max-width: 80%;
}

div.absolute {
  width: 100%;
  position: absolute;
  height: 100%;
}

div.bottom-panel-box {
  position: fixed;
  height: 350px;
  border-top: 3px solid;
  bottom: 0px;
  left: 20%;
}
</style>
