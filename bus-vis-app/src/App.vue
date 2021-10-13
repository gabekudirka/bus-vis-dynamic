<template>
  <div id="page">
    <ListContainer class="left-sidebar sidebars"/>
    <div class="main-panel">
      <div class="top-main">
        <MapPanel class="MAP" :planBusses="planBusses"> </MapPanel>
        <PlanDetails class="right-sidebar"/>
      </div>
      <BusPanel v-if="showBusses" class="bottom-main"/>
      <StationPanel v-if="!showBusses" class="bottom-main"/>
    </div>
  </div>
</template>

<script>
import BusPanel from './components/BusPanel.vue';
import StationPanel from './components/StationPanel.vue';
import MapPanel from './components/MapPanel.vue';
import PlanDetails from './components/PlanDetails.vue';
import ListContainer from './components/ListContainer.vue';
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
    ListContainer
  },
  computed: {
    showBusses: function () {
      return this.$store.state.showBusses;
    },
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
.sidebars {
  background-color: #efefef;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#page{
  display:flex;
  flex-direction:row;
  height: 100vh;
}
.left-sidebar{
  max-width:30vw;
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
  max-height:60vh;
}
.bottom-main{
  flex:1;
}
.right-sidebar{
  max-width:30vw;
  flex:1;
  overflow-y:auto;
}
.MAP{
  flex:3;
  max-height: 65vh;
}

.bottom-border{
  border-bottom: 1px solid grey;
}
</style>
