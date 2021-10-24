/* eslint-disable */
<template>
<div class="container">
    <div class="row">
        <div style="padding:1em; margin-left:auto; margin-right:auto">
            <!-- <label for="plan-select">Deployment plan:</label> -->
            <select @change="changePlan()" v-model="planselect" name="plan-select" id="plan-select">
                <option value="Plan 1">Deployment Plan 1</option>
                <option value="Plan 2">Deployment Plan 2</option>
                <option value="Plan 3">Deployment Plan 3</option>
            </select>
        </div>
    </div>
    <!-- <div id="plan-name" class="row left-align">
        <h2>{{ planselect }}</h2>
    </div> -->
    <div id="plan-details" class="row">
        <ul>
            <li>
                <p> <b>Total Cost: </b> </p>
                <p class="plan-data"> {{ planCost }} </p>
            </li>
            <li>
                <p> <b> Total Environmental Equity: </b> </p>
                <p class="plan-data"> {{ planData.env_equity }} </p>
            </li>
            <li>
                <p> <b> Buses Converted: </b> </p>
                <p class="plan-data"> {{ planData.num_buses }} </p>
            </li>
            <li>
                <p> <b> Daily Miles Electrified: </b> </p>
                <p class="plan-data"> {{ planData.num_miles }} </p>
            </li>
            <li>
                <p> <b> Charging Stations: </b> </p>
                <p class="plan-data"> {{ planData.num_charging_stations }} </p>
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
            planData: p20
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
        }
    }
};
</script>

<style>
ul {
    padding: 0;
    list-style-type: none;
}
#plan-details{
    display:block;
    text-align:center;
    margin-left:auto;
    margin-right:auto;
    padding-top:15px;
}
p{
    margin-bottom:0.25em !important;
}
select {
    border-radius: 8px;
    border: none;
    padding: 7px;
    background-color: #efefef;
}   
select:focus-visible {
    outline: none
}
option {
    font-size:12pt;
}
.plan-data {
    padding-top:0;
    font-size: 16pt;
    font-family:'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    color:#4f4f4f;
    padding-bottom:5px;
}
.container {
    display:block;
}
</style>
