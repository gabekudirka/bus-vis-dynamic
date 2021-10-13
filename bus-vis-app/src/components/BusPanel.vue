/* eslint-disable */
<template>
  <div class="container-fluid bottom-panel-box">
    <div class="row">
      <div class="col-5 left-align">
          <h4>
            <i class="fas fa-bus"></i>
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
