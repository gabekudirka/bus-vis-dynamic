<template>
  <div id="page">
    <RoutesList class="left-sidebar"/>
    <div class="main-panel">
      <div class="top-main bottom-border">
        <MapPanel class="MAP" :planBusses="planBusses"> </MapPanel>
        <div class="MAP">
          <BusMap />
        </div>
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
import MapPanel from './components/MapPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import RoutesList from './components/RoutesList.vue';
import BusMap from './components/BusMap.vue';
import p20 from './data/plans/p20.json';
import p60 from './data/plans/p60.json';
import p180 from './data/plans/p180.json';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'App',
  components: {
    BusPanel,
    StationPanel,
    MapPanel,
    PlanDetails,
    RoutesList,
    BusMap
  },
  data() {
    return {
      showBus: true,
    };
  },
  computed: {
    planBusses: function () {
        if (this.$store.state.plan === 'p20') {
            return p20;
        } if (this.$store.state.plan === 'p60') {
            return p60;
        }
        return p180;
    },
  }
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
  max-width:450px;
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
  max-width:450px;
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
