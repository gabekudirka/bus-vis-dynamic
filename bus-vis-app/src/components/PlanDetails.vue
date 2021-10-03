/* eslint-disable */
<template>
<div class="container side-panel-box">
    <div class="row plan-select-row">
        <div>
            <label for="plan-select">Select a deployment plan:</label>
            <select name="plan-select" id="plan-select">
                <option value="Plan1">Plan 1</option>
                <option value="Plan2">Plan 2</option>
                <option value="Plan3">Plan 3</option>
            </select>
        </div>
    </div>
    <div class="row">
        <h2 id="plan">{{message}}</h2>
    </div>
    <div class="row">
        <div>
        <ul>
            <li>
                <p>Total Cost of the plan</p>
            </li>
            <li>
                <p>Total Environment Equity Score</p>
            </li>
            <li>
                <p>Number of buses converted</p>
            </li>
            <li>
                <p>Charging stations to be built</p>
            </li>
            <li>
                <p>Total miles electrified</p>
            </li>
        </ul>
    </div>
    </div>
</div>
</template>

<script>

export default {
  name: 'PlanDetails',
  data() {
      return {
        message: 'Hello Vue!',
      };
  }
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

</style>
