<template>
  <div id="page">
    <ListContainer class="left-sidebar sidebars" :key="plan" :planBusses="planBusObj" :planObj="planObj"/>
    <div class="main-panel">
      <div class="top-main">
        <MapPanel class="MAP panel" :planObj="planBusObj"> </MapPanel>
        <PlanDetails class="right-sidebar panel"/>
      </div>
      <BusPanel v-if="showBusses" :key="plan" :planObj="planObj" :planBusObj="planBusObj" class="bottom-main panel"/>
      <StationPanel v-if="!showBusses" :key="plan" :planObj="planObj" class="bottom-main panel"/>
    </div>
  </div>
</template>

<script>
import BusPanel from './components/BusPanel.vue';
import StationPanel from './components/StationPanel.vue';
import MapPanel from './components/MapPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import ListContainer from './components/ListContainer.vue';
import p20p from './data/plans/p20.json';
import p60p from './data/plans/p60.json';
import p180p from './data/plans/p180.json';
import p20b from './data/buses/p20.json';
import p60b from './data/buses/p60.json';
import p180b from './data/buses/p180.json';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default {
  name: 'App',
  components: {
    BusPanel,
    StationPanel,
    MapPanel,
    PlanDetails,
    ListContainer
  },
  computed: {
    plan: function () {
      return this.$store.state.plan;
    },
    showBusses: function () {
      return this.$store.state.showBusses;
    },
    planBusObj: function () {
        if (this.plan === 'p20') {
            return p20b;
        } if (this.plan === 'p60') {
            return p60b;
        }
        return p180b;
    },
    planObj: function () {
      if (this.plan === 'p20') {
            return p20p;
        } if (this.plan === 'p60') {
            return p60p;
        }
        return p180p;
    }
  },
  // watch: {
  //       plan: function () {
  //         // TODO set charging station to planObj.cs[0] and bus to planBusObj.buses[0]
  //         console.log(this.planObj.chargingStations[0]);
  //         this.$store.dispatch('changeStation', this.planObj.chargingStations[0].stop_id);
  //         console.log(this.planBusObj.buses[0]);
  //         this.$store.dispatch('changeBus', this.planBusObj.buses[0].id);
  //       }
  //   },
};
</script>

<style>
body{
  background-color: #e8f3f2;
}
.sidebars {
  background-color: #efefef;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: 11pt;
}
#page{
  display:flex;
  flex-direction:row;
  height: 100vh;
  overflow-y: hidden;
  overflow-x: hidden;
}
.left-sidebar{
  width:20vw;
  flex:1;
  overflow-y:auto;
  height:100%;
  position: fixed;
  z-index:1;
  top: 0;
  left: 0;
}
.panel{
  background-color: #fff;
  margin: .25em;
  padding: .25em;
  filter: drop-shadow(1px 1px 3px #dfdfdf);
  border-radius: 5px;
}
.main-panel{
  flex:3;
  display:flex;
  flex-direction:column;
  margin-left: 20vw;
}
.top-main{
  flex:4;
  display: flex;
}
.bottom-main{
  flex:1;
  min-height: 27vh;
  overflow-y: auto;
  overflow-x: hidden;
}
.right-sidebar{
  flex:1;
  max-width: 15vw; 
  overflow-y: auto;
  overflow-x: hidden;
}
.MAP{
  flex:3;
}
.bottom-border{
  border-bottom: 1px solid grey;
}
</style>
