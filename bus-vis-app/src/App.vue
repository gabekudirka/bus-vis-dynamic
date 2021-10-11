<template>
  <div id="page">
    <RoutesList class="left-sidebar"/>
    <div class="main-panel">
      <div class="top-main bottom-border">
        <div class="MAP"> </div>
        <PlanDetails class="left-border right-sidebar"/>
      </div>
      <BusPanel v-if="showBus === true" class="bottom-main"/>
      <StationPanel v-if="showBus === false" class="bottom-main"/>
    </div>
  </div>
</template>

<script>
import BusPanel from './components/BusPanel.vue';
import StationPanel from './components/StationPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import RoutesList from './components/RoutesList.vue';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'App',
  components: {
    BusPanel,
    StationPanel,
    PlanDetails,
    RoutesList
  },
  data() {
    return {
      showBus: true,
    };
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
  height: 90vh;
}
.left-sidebar{
  flex:1;
  overflow-y:auto;
  height:100%;
}

.main-panel{
  flex:3;
  display:flex;
  flex-direction:column;
}
.top-main{
  flex:4;
  display: flex;
  height:100%;
}
.bottom-main{
  flex:1;
}
.right-sidebar{
  flex:1;
  overflow-y:auto;
  height:100%;
}
.MAP{
  flex:3;
}
.left-border{
  border-left: 1px solid grey;
}
.bottom-border{
  border-bottom: 1px solid grey;
}
</style>
