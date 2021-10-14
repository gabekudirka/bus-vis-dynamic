/* eslint-disable */
<template>
  <div class="container-fluid bottom-panel-box">
    <div class="row">
      <div class="col-5 left-align">
          <h4>
            <i v-if="bus.converted" class="fas fa-plug" style="padding:.1em"></i>
            <i class="fas fa-bus" style="padding:.1em"></i>
            Bus {{ bus.id }} 
          </h4>
          <p> Bus Line: {{ bus.line }} </p>
          <p> Converted: {{ bus.converted }} </p>
          <p> Bus Status: On Route </p>
          <p> Last Stop: {{ bus.stops[0].stop_name }} </p>
          <p> Bus Environmental Impact: {{ bus.environmental_equity }} </p>
      </div>
      <div class="col">
         <p> <b> Charge level over time </b> </p>
         <div id="charge-chart-container">

         </div>
      </div>
      <div class="col"><b> Electricity usage </b></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'BusPanel',
    props: {
        planObj: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            width: 750,
            height: 400,
            margin: {
                top: 50,
                right: 50,
                left: 50,
                bottom: 50,
            },
        };
    },
    computed: {
        busId: function () {
            return this.$store.state.selectedBus;
        },
        bus: function () {
            return this.planObj.buses.find((bus) => bus.id === this.busId);
        },
        chargeChartData: function () {
            const chargeData = [];
            for (let i = 0; i < this.bus.stops.length; i++) {
                if (i === 0) {
                    chargeData.push({ time: this.bus.stops[i].departure_time, charge: Math.max(0, parseInt(this.bus.stops[i].remaining_charge, 10)) });
                } else {
                    chargeData.push({ time: this.bus.stops[i].arrival_time, charge: Math.max(0, parseInt(this.bus.stops[i].remaining_charge, 10)) });
                }
            }
            return chargeData;
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
        init() {
            // const data = this.timex.map((el, index) => [el, this.chargeChartData[index]]);
            const svg = d3
            .select('#charge-chart-container')
            .append('svg')
                .attr('width', this.width)
                .attr('height', this.height)
            .append('g')
            .style(
                'transform',
                `translate(${this.margin.left}px, ${this.margin.top}px)`
            );

            return svg;
            // const xAccessor = (pt) => pt.time;
            // const yAccessor = (pt) => pt.charge;

            // const yScale = d3
            //     .scaleLinear()
            //     .domain(d3.extent(this.chargeChartData))
            //     .range([0, 100]);
            // const xScale = d3
            //     .scaleTime()
            //     .domain(d3.extent(this.timeX))
            //     .range([0, 1]);

            // const line = d3
            //     .line()
            //     .x((d) => xScale(xAccessor(d)))
            //     .y((d) => yScale(yAccessor(d)));

            // svg
            //     .append('path')
            //     .attr('d', line(data))
            //     .attr('fill', 'none')
            //     .attr('stroke', 'rgb(34 150 243)')
            //     .attr('stroke-width', 3);
        //     const yAxisGenerator = d3
        //         .axisLeft()
        //         .scale(yScale)
        //         .ticks(5);

        //     svg.append('g').call(yAxisGenerator);

        //     const xAxisGenerator = d3
        //         .axisBottom()
        //         .scale(xScale)
        //         .ticks(5);

        //     svg
        //         .append('g')
        //         .call(xAxisGenerator);
        }
    },
    mounted() {
        this.init();
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
