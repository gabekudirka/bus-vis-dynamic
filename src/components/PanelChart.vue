<template>
    <svg :viewBox="viewBox">
        <g v-bind:id="chartName" transform="translate(35, 5)"> </g>
    </svg>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'PanelChart',
    props: {
        data: {
            required: true,
            type: Array,
        },
        chartName: {
            required: true,
            type: String,
        },
        containerWidth: {
            default: 375,
            type: Number,
        },
        containerHeight: {
            default: 210,
            type: Number,
        }
    },
    data() {
        return {
            margin: { 
                top: 15, 
                right: 35, 
                bottom: 40, 
                left: 25 
            },
            innerClass: `${this.chartName}-data`,
        };
    },
    computed: {
        width: function () {
            return this.containerWidth - this.margin.left - this.margin.right;
        },
        height: function () {
            return this.containerHeight - this.margin.top - this.margin.bottom;
        },
        viewBox: function () {
            return `0 0 ${this.containerWidth} ${this.containerHeight}`;
        },
    },
    watch: {
        data: function () {
            this.clearChart();
            this.renderCharts();
        }
    },
    methods: {
        renderCharts() {
            const timeParser = d3.timeParse('%H:%M');
            const xAccessor = (pt) => timeParser(pt.x);
            const yAccessor = (pt) => pt.y;

            const xScale = d3.scaleTime().range([0, this.width]);
            const yScale = d3.scaleLinear().range([this.height, 0]);

            const line = d3.line()
                .x((d) => xScale(xAccessor(d)))
                .y((d) => yScale(yAccessor(d)));

            const xAxis = d3.axisBottom()
                        .scale(xScale)
                        .ticks(8)
                        .tickFormat(d3.timeFormat('%H:%M'));
            
            const yAxis = d3.axisLeft()
                        .scale(yScale)
                        .ticks(8); 

            switch (this.chartName) {
                case ('charge-chart'):
                    yAxis.tickFormat((t) => `${t}%`);
                    xScale.domain(d3.extent(this.data, xAccessor));
                    yScale.domain([0, d3.max(this.data, yAccessor)]);
                    break;
                case ('miles-chart'):
                    xScale.domain(d3.extent(this.data, xAccessor));
                    if (d3.max(this.data, yAccessor) <= 200) {
                        yScale.domain([0, 200]);
                    } else {
                        const domainMax = d3.max(this.data, yAccessor);
                        yScale.domain([0, (domainMax + (20 - (domainMax % 20)))]);
                    }
                    break;
                case ('stations-chart'):
                    xScale.domain(d3.extent(this.data, xAccessor));
                    if (d3.max(this.data, yAccessor) <= 35) {
                        yScale.domain([0, 35]);
                    } else {
                        const domainMax = d3.max(this.data, yAccessor);
                        yScale.domain([0, (domainMax + (20 - (domainMax % 20)))]);
                    }
                    break;
                default:
                    break;
            }

            const svg = d3.selectAll(`#${this.chartName}`);
            svg.append('path')
                .classed(this.innerClass, true)
                .attr('d', line(this.data))
                .attr('fill', 'none')
                .attr('stroke', 'rgb(34 150 243)')
                .attr('stroke-width', 3);
            svg.append('g')
                .classed(this.innerClass, true)
                .call(xAxis)
                .style('transform', `translateY(${this.containerHeight - this.margin.top - this.margin.bottom}px)`);
            svg.append('g')
                .classed(this.innerClass, true)
                .call(yAxis);
        },
        clearChart() {
            d3.selectAll(`.${this.innerClass}`).remove();
        }
    },
    mounted() {
        this.renderCharts();
    }
};

</script>
