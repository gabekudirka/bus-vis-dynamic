/* eslint-disable */
<template>
<div class="container side-panel-box">
    <div class="row plan-select-row">
        <div>
            <label for="plan-select">Select a deployment plan:</label>
            <select  v-model="planselect" name="plan-select" id="plan-select">
                <option value="Plan 1">Plan 1</option>
                <option value="Plan 2">Plan 2</option>
                <option value="Plan 3">Plan 3</option>
            </select>
        </div>
    </div>
    <div class="row">
        <h2 id="plan">{{ planselect }}</h2>
    </div>
    <div id="plan-details" class="row">
        <div>
        <ul id="plan-list">
            <li>
                <p>Total Cost of the plan</p>
            </li>
            <li>
                <p>Plan Environmental Equity:<br> {{ planData.env_equity }}</p>
            </li>
            <li>
                <p>Number of buses converted:<br> {{ planData.num_buses }}</p>
            </li>
            <li>
                <p>Total miles electrified:<br>{{ planData.num_miles }}</p>
            </li>
            <li>
                <p>Number of charging stations to be built:<br> {{ planData.num_charging_stations }}</p>
            </li>
            <li>
                <p>Locations of charging locations</p>
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
            planselect: '',
            p20,
            p60,
            p180,
        };
    },
    computed: {
        planData: function () {
            if (this.planselect === 'Plan 1') {
                return p20;
            } if (this.planselect === 'Plan 2') {
                return p60;
            } if (this.planselect === 'Plan 3') {
                return p180;
            }
                return p20;
        }
    },
};

</script>

<style>

div.plan-select-row {
    padding-top: 10px;
}

div.side-panel-box {
    width: 20%;
    position: fixed;
    bottom: 350px;
    top: 0;
    right: 0;
    border-left: 3px solid;
}

ul {
    padding: 0;
    list-style-type: none;
}

#plan-list {
    height: 450px;
}

#charging-station-locations {
    height: 300px;
}

.scroll {
    overflow: hidden;
    overflow-y: scroll;
}

</style>
