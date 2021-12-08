/* eslint-disable */
<template>
    <div class="left-align" style="padding:1em">    
        <div class="row1">
            <div class="left-align flex1 col-3">
                <h4>
                    <i v-if="bus.converted" class="fas fa-plug" style="padding:.1em"></i>
                    <i class="fas fa-bus" style="padding:.1em"></i>
                    Bus {{ bus.id }} 
                </h4>
                <p> <b> Bus Line: </b> {{ bus.line }} </p>
                <p> <b> {{ converted }} </b> </p>
                <p> <b> Bus Status: </b> {{ busStatus }} </p>
                <!-- <p> Last Stop: {{ bus.stops[0].stop_name }} </p> -->
                <p> <b> Bus Environmental Impact: </b> {{ bus.environmental_equity }} </p>
            </div>
            <div class="flex1">
                <div id="miles-chart-container" class="chart">
                    <p class="chart-title"> <b> Miles Driven </b> </p>
                    <PanelChart
                        :data="milesChartData"
                        :chartName="'miles-chart'"
                        :containerWidth="chartSize.width"
                        :containerHeight="chartSize.height"
                    />
                </div>
            </div>
            <div class="flex1">
                <div v-show="bus.converted" id="charge-chart-container" class="chart">
                    <p class="chart-title"> <b> Charge level over time </b> </p>
                    <PanelChart
                        :data="chargeChartData"
                        :chartName="'charge-chart'"
                        :containerWidth="chartSize.width"
                        :containerHeight="chartSize.height"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PanelChart from './PanelChart.vue';
import stopsList from '../data/allStops.json';

export default {
    name: 'BusPanel',
    components: {
        PanelChart,
    },
    props: {
        planBusObj: {
            type: Object,
            required: true
        },
        planObj: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            chartSize: {
                height: 210,
                width: 400
            }
        };
    },
    computed: {
        busId: function () {
            return this.$store.state.selectedBus;
        },
        bus: function () {
            return this.planBusObj.buses.find((bus) => bus.id === this.busId);
        },
        converted: function () {
            return this.bus.converted ? 'Converted Bus' : 'Not Converted';
        },
        chargeChartData: function () {
            const chargeData = [];
            chargeData.push({ x: '03:00', y: 100 });
            for (let i = 0; i < this.bus.stops.length; i++) {
                if (i === 0) {
                    if (this.bus.stops[i].departure_time > '3:00') {
                        chargeData.push({ x: '3:00', y: Math.max(0, parseInt(this.bus.stops[i].remaining_charge, 10)) });
                    }
                    chargeData.push({ x: this.bus.stops[i].departure_time, y: Math.max(0, parseInt(this.bus.stops[i].remaining_charge, 10)) });
                } else {
                    chargeData.push({ x: this.bus.stops[i].arrival_time, y: Math.max(0, parseInt(this.bus.stops[i].remaining_charge, 10)) });
                }
            }
            const finalTime = this.bus.stops[this.bus.stops.length - 1].arrival_time;
            chargeData.push({ x: finalTime > '23:00' ? finalTime : '23:00', y: Math.max(0, parseInt(this.bus.stops[this.bus.stops.length - 1].remaining_charge, 10)) });
            return chargeData;
        },
        milesChartData: function () {
            const milesData = [];
            let totalMiles = 0;
            for (let i = 0; i < this.bus.stops.length; i++) {
                if (i === 0) {
                    if (this.bus.stops[i].departure_time > '3:00') {
                        milesData.push({ x: '3:00', y: totalMiles });
                    }
                    milesData.push({ x: this.bus.stops[i].departure_time, y: totalMiles });
                } else {
                    if (this.bus.stops[i].distance_traveled !== 0) {
                        totalMiles += this.bus.stops[i].distance_traveled - this.bus.stops[i - 1].distance_traveled;
                    }
                    milesData.push({ x: this.bus.stops[i].arrival_time, y: totalMiles });
                }
            }
            const finalTime = this.bus.stops[this.bus.stops.length - 1].arrival_time;
            milesData.push({ x: finalTime > '23:00' ? finalTime : '23:00', y: totalMiles });
            return milesData;
        },
        busStatus: function () {
            if (this.$store.state.busLocations.features.length > 1) {
                const busob = this.$store.state.busLocations.features.find((bus) => bus.properties.id === this.busId);
                if (busob.properties.atStation) {
                    return 'At Stop';
                } else {
                    return 'On Route';
                }
            } else {
                return 'At Stop';
            }
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
        },
    }
};
</script>

<style>
.row1{
    display: flex;
    flex-direction:row;
    flex-wrap:wrap;
}
.left-align{
    text-align: left;
    padding-left:1em;
}
.flex1{
    flex:1;
}
.chart-title{
    text-align: center;
}
p{
    margin: 0.2em !important;
}
.chart{
    max-width:31vw;
}
</style>
