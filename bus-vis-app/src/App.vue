<template>
  <div>
    <PlanDetails />
    <BusPanel />
  </div>
</template>

<script>
import BusPanel from './components/BusPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'App',
  components: {
    BusPanel,
    PlanDetails,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
