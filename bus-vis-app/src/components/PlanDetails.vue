/* eslint-disable */
<template>
<div class="container side-panel-box">
    <div class="row">
        <div style="padding:1em">
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
    <div id="plan-details" class="row left-align">
        <ul>
            <li>
                <p> <b>Total Cost of the plan: </b> <br> {{ planCost }} </p>
            </li>
            <li>
                <p> <b> Plan Environmental Equity: </b> <br> {{ planData.env_equity }}</p>
            </li>
            <li>
                <p> <b> Number of buses converted: </b> <br> {{ planData.num_buses }}</p>
            </li>
            <li>
                <p> <b> Total miles electrified: </b> <br>{{ planData.num_miles }}</p>
            </li>
            <li>
                <p> <b> Number of charging stations to be built: </b> <br> {{ planData.num_charging_stations }}</p>
            </li>
            <li>
                <p><b> Locations of charging locations: </b></p>
                <ul id="charging-station-locations" class="scroll">
                    <li v-for="station in planData.charging_stations" :key="station.stop_name">
                        {{station.num_stations}} station built at {{ station.stop_name }}
                    </li>
                </ul>
                <br>
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

#charging-station-locations {
    /* This should be changed to be dynamic*/
    height: 300px;
}

#plan-name {
    text-align: left;
    padding-left: 1em;
    padding-bottom: 0.25em;
}

.scroll {
    overflow-x: hidden;
    overflow-y: auto;
}

.left-align{
    text-align: left;
    padding: 1em;
}

p{
    margin-bottom:0.5em !important;
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
</style>
