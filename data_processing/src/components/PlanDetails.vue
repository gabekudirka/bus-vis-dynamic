/* eslint-disable */
<template>
<div class="container">
    <div class="row">
        <div style="padding:0.5em; margin-left:auto; margin-right:auto">
            <!-- <label for="plan-select">Deployment plan:</label> -->
            <select @change="changePlan()" v-model="planselect" name="plan-select" id="plan-select">
                <option value="Plan 1">Deployment Plan 1</option>
                <option value="Plan 2">Deployment Plan 2</option>
                <option value="Plan 3">Deployment Plan 3</option>
            </select>
            <select v-show="compare" @change="changeComparePlan()" v-model="compareSelect" name="compare-select" class="compare-select" style="margin-top:0.3em">
                <option value="Plan 1">Deployment Plan 1</option>
                <option value="Plan 2">Deployment Plan 2</option>
                <option value="Plan 3">Deployment Plan 3</option>
            </select>
            <div v-show="!compare" class="blueUnd" @click="compare=true">+Compare Plan</div>
            <div v-show="compare" class="blueUnd" @click="compare=false">-Hide Comparison</div>
        </div>
    </div>
    <!-- <div id="plan-name" class="row left-align">
        <h2>{{ planselect }}</h2>
    </div> -->
    <div id="plan-details" class="row">
        <ul style="padding-left:0.5em">
            <li>
                <p class="label"> <b>Total Cost: </b> </p>
                <p class="plan-data"><span v-show="compare" class="smaller">Selected Plan: </span> {{ planCost }} </p>
                <p v-show="compare" class="plan-data compare-data"><span class="smaller">Comparison:</span> {{ compareCost }} </p>
            </li>
            <li>
                <p class="label"> <b> Total Environmental Equity: </b> </p>
                <p class="plan-data"><span v-show="compare" class="smaller">Selected Plan: </span> {{ planData.env_equity }} </p>
                <p v-show="compare" class="plan-data compare-data"><span class="smaller">Comparison: </span>{{ compareData.env_equity }} </p>
            </li>
            <li>
                <p class="label"> <b> Buses Converted: </b> </p>
                <p class="plan-data"><span v-show="compare" class="smaller">Selected Plan: </span> {{ planData.num_buses }} </p>
                <p v-show="compare" class="plan-data compare-data"><span class="smaller">Comparison: </span>{{ compareData.num_buses }} </p>
            </li>
            <li>
                <p class="label"> <b> Daily Miles Electrified: </b> </p>
                <p class="plan-data"><span v-show="compare" class="smaller">Selected Plan: </span> {{ planData.num_miles }} </p>
                <p v-show="compare" class="plan-data compare-data"><span class="smaller">Comparison: </span>{{ compareData.num_miles }} </p>
            </li>
            <li>
                <p class="label"> <b> Charging Stations: </b> </p>
                <p class="plan-data"><span v-show="compare" class="smaller">Selected Plan: </span> {{ planData.num_charging_stations }} </p>
                <p v-show="compare" class="plan-data compare-data"><span class="smaller">Comparison: </span>{{ compareData.num_charging_stations }} </p>
            </li>
        </ul>
    </div>
</div>
</template>

<script>
import p20 from '../data/plans/p20.json';
import p60 from '../data/plans/p60.json';
import p180 from '../data/plans/p180.json';

export default {
    name: 'PlanDetails',
    data() {
        return {
            p20,
            p60,
            p180,
            planselect: 'Plan 1',
            planCost: '$20,000,000',
            planData: p20,
            compare: false, // toggles plan comparison on and off
            compareSelect: 'Plan 2',
            compareCost: '$60,000,000',
            compareData: p60,
        };
    },
    methods: {
        changePlan() {
            switch (this.planselect) {
                case 'Plan 1':
                    this.planData = p20;
                    this.planCost = '$20,000,000';
                    this.$store.dispatch('changePlan', 'p20');
                    break;
                case 'Plan 2':
                    this.planData = p60;
                    this.planCost = '$60,000,000';
                    this.$store.dispatch('changePlan', 'p60');
                    break;
                case 'Plan 3':
                    this.planData = p180;
                    this.planCost = '$180,000,000';
                    this.$store.dispatch('changePlan', 'p180');
                    break;
                default:
                    break;
            }
        },
        changeComparePlan() {
            switch (this.compareSelect) {
                case 'Plan 1':
                    this.compareData = p20;
                    this.compareCost = '$20,000,000';
                    break;
                case 'Plan 2':
                    this.compareData = p60;
                    this.compareCost = '$60,000,000';
                    break;
                case 'Plan 3':
                    this.compareData = p180;
                    this.compareCost = '$180,000,000';
                    break;
                default:
                    break;
            }
        }
    }
};
</script>

<style>
ul {
    padding: 0;
    list-style-type: none;
    margin-bottom:0 !important;
}
#plan-details{
    display:block;
    /* text-align:center; */
    margin-left:auto;
    margin-right:auto;
    /* padding-top:15px; */
}
.blueUnd {
    color: lightseagreen;
    cursor: pointer;
    text-align: right;
    font-size: smaller;
    padding-top: 0.5em;
    padding-right: 0.5em;
}
.blueUnd:hover{
    text-decoration: underline;
}
.smaller{
    font-size:smaller;
}
p{
    margin-bottom:0.25em !important;
}
.label{
    text-align: left;
    padding-top:0.5em;
}
.compare-select{
    background-color: #cdeceb !important;
}
select {
    border-radius: 8px;
    border: none;
    padding: 7px;
    background-color: #efefef;
    overflow: hidden;
    white-space: pre;
    text-overflow: ellipsis;
    max-width: 20vw;
}   
select:focus-visible {
    outline: none
}
option {
    font-size:12pt;
}
.plan-data {
    padding-top:0;
    padding-left: 1em;
    font-size: larger;
    font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    color:#4f4f4f;
    /* padding-bottom:5px; */
    text-align:left
}
.compare-data{
    color:lightseagreen;
}
.container {
    display:block;
}
</style>
