<template>
    <div id="vis">
        <i class="fas fa-play" id="play-button"></i>
        <svg id="slider-svg" :viewBox="viewBox"></svg>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'TimeSlider',
    data() {
        return {
            margin: {
                top: 50, 
                right: 50, 
                bottom: 0, 
                left: 50
            },
            containerWidth: 960,
            containerHeight: 100,
            timer: 0,
            currentValue: 0,
            moving: false,
            slider: null,
            handle: null,
            label: null,
            coef: 1000 * 60 * 10,
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
        startTime: function () {
            const timeParser = d3.timeParse('%H:%M');
            return timeParser('00:00');
        },
        endTime: function () {
            const timeParser = d3.timeParse('%H:%M');
            return timeParser('23:59');
        },
        xScale: function () {          
            return d3.scaleTime()
                .domain([this.startTime, this.endTime])
                .range([0, this.width])
                .clamp(true);
        },
        svg: function () {
            return d3.select('#slider-svg');
        },
        playButton: function () {
            return d3.select('#play-button');
        },
    },
    watch: {
        currentValue: function (val) {
            const getTime = d3.timeFormat('%H:%M');
            const timeString = getTime(this.xScale.invert(val));
            const minutes = Math.floor(parseInt(timeString.substring(3), 10) / 10) * 10;
            const roundedTime = minutes !== 0 ? timeString.substring(0, 3) + minutes.toString() : timeString.substring(0, 3) + '00';
            this.$store.dispatch('changeTime', roundedTime);
        }
    },
    methods: {
        update: function update(pos) {
            // update position and text of label according to slider scale
            const formatTime = d3.timeFormat('%H:%M');
            this.handle.attr('cx', this.xScale(pos));
            this.label
                .attr('x', this.xScale(pos))
                .text(formatTime(pos));
        },
        renderSlider() {
            const formatTime = d3.timeFormat('%H:%M');

            this.slider = this.svg.append('g')
                .attr('class', 'slider')
                .attr('transform', `translate(${this.margin.left},40)`);

            this.slider.append('line')
                .attr('class', 'track')
                .attr('x1', this.xScale.range()[0])
                .attr('x2', this.xScale.range()[1])
            .select(function () { return this.parentNode.appendChild(this.cloneNode(true)); })
                .attr('class', 'track-inset')
            .select(function () { return this.parentNode.appendChild(this.cloneNode(true)); })
                .attr('class', 'track-overlay')
                .call(d3.drag()
                    .on('start.interrupt', () => { this.slider.interrupt(); })
                    .on('start drag', (event, d) => {
                        this.currentValue = event.x;
                        this.update(this.xScale.invert(this.currentValue)); 
                    }));

            this.slider.insert('g', '.track-overlay')
                .attr('class', 'ticks')
                .attr('transform', `translate(0,${18})`)
            .selectAll('text')
                .data(this.xScale.ticks(13)) // changes step in labels
                .enter()
                .append('text')
                .attr('x', this.xScale)
                .attr('y', 10)
                .attr('text-anchor', 'middle')
                .text((d) => formatTime(d));

            this.handle = this.slider.insert('circle', '.track-overlay')
                .attr('class', 'handle')
                .attr('r', 10);

            this.label = this.slider.append('text')  
                .attr('class', 'label')
                .attr('text-anchor', 'middle')
                .text(formatTime(this.startTime))
                .attr('transform', `translate(0,${-25})`);
        },
        renderPlayButton() {
            let timer = 0;
            const ref = this;
            
            const step = function () {
                ref.update(ref.xScale.invert(ref.currentValue));
                ref.currentValue += (ref.width / 151);
                if (ref.currentValue > ref.width) {
                    ref.moving = false;
                    ref.currentValue = 0;
                    clearInterval(timer);
                    ref.attr('class', 'fas fa-play');
                }
            };
            
            this.playButton.on('click', function () {
                const button = d3.select(this);
                if (this.moving) {
                    this.moving = false;
                    clearInterval(timer);
                    button.attr('class', 'fas fa-play');
                } else {
                    this.moving = true;
                    timer = setInterval(step, 100);
                    button.attr('class', 'fas fa-pause');
                }
            });
        }
    },
    mounted() {
        this.renderSlider();
        this.renderPlayButton();
    }
};
</script>

<style>
    #vis{
        padding-top: 2px;
        display: flex;
        align-items: center;
        width: 72%;
        margin: auto;
    }
    #play-button {
      margin-right:1em;
      margin-bottom: 0.8em;
      color: lightseagreen;
      cursor: pointer;
      font-size: 20pt;
    }
    #play-button:hover {
      color: #696969;
    } 
    .label {
        font-size: 11pt;
    }
    .ticks {
      font-size: 10pt;
      padding-top:0.5em;
    }
    .track,
    .track-inset,
    .track-overlay {
      stroke-linecap: round;
    }
    .track {
      stroke: #696969;
      stroke-opacity: 0.3;
      stroke-width: 10px;
    }
    .track-inset {
      stroke: #efefef;
      stroke-width: 8px;
    }
    .track-overlay {
      pointer-events: stroke;
      stroke-width: 50px;
      stroke: transparent;
      cursor: crosshair;
    }
    .handle {
      fill: powderblue;
      stroke: powderblue;
      stroke-width: 5px;
    }
</style>
