<template>
  <div>
    <PlanDetails />
    <BusPanel />
    <RoutesList :plan="A" class="left-sidebar"/>
  </div>
</template>

<script>
import BusPanel from './components/BusPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import RoutesList from './components/RoutesList.vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'App',
  components: {
    BusPanel,
    PlanDetails,
    RoutesList
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
.left-sidebar{
  
}
</style>
