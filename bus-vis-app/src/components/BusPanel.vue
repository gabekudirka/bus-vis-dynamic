/* eslint-disable max-len */
<template>
  <div class="container bottom-panel-box">
    <div class="row absolute">
      <div class="col-5 border">
        <div class="row border">
            {{ bus.environmental_equity }}
        </div>
        <div class="row border">
          <div class="col border">rrr</div>
          <div class="col border">text column</div>
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
            busId: '1026',
            p20
        };
    },
    computed: {
        bus: function () {
            return this.p20Dict[this.busId];
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
