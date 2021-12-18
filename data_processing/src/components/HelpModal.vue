<!-- ADD PHOTOS TO DESCRIPTIONS -->
<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <div> User Guide </div>
        <i class="fas fa-times btn-close" 
            @click="close">
        </i>
      </header>

      <section class="modal-body">
        <h2>Features:</h2>
        <div> 
            <div class="section">
                <h3 @click="showLeftSide=!showLeftSide">
                    <i v-show="!showLeftSide" class="fas fa-chevron-down"></i>
                    <i v-show="showLeftSide" class="fas fa-chevron-up"></i>
                    Left Sidebar
                </h3>
                <div v-show="showLeftSide">
                    <li>Use Stations/Busses toggle to view and select Charging Stations vs Busses.</li>
                    <li>Buses can be sorted by feature by clicking any of the header features (e.g. busNo, line, etc) above the list </li>
                    <li>Buses can be shown/hidden from map using the checkboxes to the left of the list item</li>
                    <li>The checkbox at the top will toggle the visibiltiy of all buses</li>
                    <li>The "Show Only Converted Buses" hides non-converted buses from the buslist and map</li>
                </div>
            </div>

            <div class="section">
                <h3 @click="showMap=!showMap">
                    <i v-show="!showMap" class="fas fa-chevron-down"></i>
                    <i v-show="showMap" class="fas fa-chevron-up"></i>
                    Map Panel
                </h3>
                <div v-show="showMap">
                    <p><i class="fas fa-bus" style="color:#2a901a"></i> Converted electric buses</p>
                    <p><i class="fas fa-bus" ></i> Non-converted buses</p>
                    <p><i class="fas fa-charging-station" style="color:#2a901a"></i> Electric bus charging stations</p>
                    <li>Busses, routes, and charging stations are clickable. When a bus or station is selected, information about the bus/station will show up in the bottom panel. A selected route will turn red and the map will show only the buses currently on that route.</li>
                    <li>The layers icon on the right of the map allows users to change the map style and toggle different map features (such as air pollutant and household demographic overlays) on and off.</li>
                    <li>The time slider beneath the map allows users to move throughout the day to see bus locations change. </li>
                </div>
            </div>

            <div class="section">
                <h3 @click="showBus=!showBus">
                    <i v-show="!showBus" class="fas fa-chevron-down"></i>
                    <i v-show="showBus" class="fas fa-chevron-up"></i>
                    Bottom Panel- Bus
                </h3>
                <div v-show="showBus">
                    <li>When a bus is selected, the bottom panel will show information relevant to that bus</li>
                    <li>If it is a converted electric bus, this panel will show two charts: one representing the amount of miles the bus has driven over the course of the day, and one representing the bus's charge status throughought the day</li>
                    <li>If the bus is not converted in the selected plan, it will show only the miles driven chart </li>
                </div>
            </div>

            <div class="section">
                <h3 @click="showStation=!showStation">
                    <i v-show="!showStation" class="fas fa-chevron-down"></i>
                    <i v-show="showStation" class="fas fa-chevron-up"></i>
                    Bottom Panel- Station
                </h3>
                <div v-show="showStation">
                    <li>When a charging station is selected, the bottom panel will show information relevant to that station</li>
                    <li>Information includes UTA stop number, the list of buses currently at the station, and the current power output (at this point just the number of buses currently at station)</li>
                    <li>The chart to the left shows the number of buses at the station throughout the day</li>
                </div>
            </div>

            <div class="section">
                <h3 @click="showPlan=!showPlan">
                    <i v-show="!showPlan" class="fas fa-chevron-down"></i>
                    <i v-show="showPlan" class="fas fa-chevron-up"></i>
                    Plan Details Panel
                </h3>
                <div v-show="showPlan">
                    <li>This panel shows all static data pertaining to the implementation plan.</li>
                    <li>Plan implementations can be switched using the drop down at the top, this will update the whole screen</li>
                    <li>Clicking "+Compare Plan" will allow users to select a second plan to compare. Clicking "-Hide Comparison" will hide the comparison view.</li>
                </div>
            </div>

        </div>
       </section>

      <footer class="modal-footer">
        <button
          type="button"
          class="btn-green"
          @click="close"
        >
          Close
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Modal',
    data() {
        return {
            showLeftSide: false,
            showMap: false,
            showBus: false, 
            showStation: false,
            showPlan: false
        };
    },
    methods: {
      close() {
        this.$emit('close');
      },
    },
  };
</script>

<style>
h2 {
    font-size: 1.5rem !important;
    font-weight: bold !important;
}
h3 {
    font-size:1.15rem !important;
}
li {
  padding:0.2rem;
  padding-left: 0.4rem;
}
.section {
    background-color: #e5efee;
    border-radius: 10px;
    padding:1em;
    margin:0.5em;
    display: block !important;
}
.fa-chevron-down, .fa-chevron-up {
    font-size: smaller;
    color: lightgrey;
}
.fa-bus, .fa-charging-station{
    padding: 0.1em;
}
  .modal-backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    /* justify-content: center;
    align-items: center; */
    text-align: left;
  }

  .modal {
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex !important;
    flex-direction: column;
  }

  .modal-header,
  .modal-footer {
    padding: 15px;
    display: flex;
  }

  .modal-header {
    position: relative;
    border-bottom: 1px solid #eeeeee;
    /* color: lightseagreen; */
    justify-content: space-between;
  }

  .modal-footer {
    border-top: 1px solid #eeeeee;
    flex-direction: column;
    justify-content: flex-end;
  }

  .modal-body {
    position: relative;
    /* padding: 30px 20px; */
    margin: 1em 2em;
    overflow-x: auto;
  }

.btn-close {
    position: absolute;
    top: 0;
    right: 0;
    border: none;
    font-size: 20px;
    padding: 10px;
    cursor: pointer;
    font-weight: bold;
    color: lightseagreen;
    background: transparent;
}

.btn-green {
    color: white;
    background: lightseagreen;
    border: 1px solid lightseagreen;
    border-radius: 2px;
}
  
</style>
