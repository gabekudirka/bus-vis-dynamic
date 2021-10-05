<template>
  <div id="page">
    <RoutesList :plan="A" class="left-sidebar"/>
    <div class="main-panel">
      <div class="top-main">
        <div class="MAP"> </div>
        <PlanDetails />
      </div>
      <BusPanel class="bottom-main"/>
    </div>
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
#page{
  display:flex;
  flex-direction:row;
}
.left-sidebar{
  flex:1;
}
.main-panel{
  flex:4;
  display:flex;
  flex-direction:column;
}
.MAP{
  flex:4;
}
.bottom-main{
  flex:1;
}
</style>
