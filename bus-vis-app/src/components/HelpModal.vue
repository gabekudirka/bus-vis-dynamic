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
                    <p> Use Stations/Busses toggle to view and select Charging Stations vs Busses.</p>
                    <p>Buses can be sorted by clicking the "busNo", "route", etc. headers above the list </p>
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
                    <p>The layers icon on the right of the map allows users to change the map style and toggle different map features on and off.</p>
                    <p>Busses, routes, and charging stations are clickable and will select the chosen station or bus in the bottom panel.</p>
                    <p>The time slider beneath the map allows users to move throughout the day to see bus locations change. </p>
                </div>
            </div>

            <div class="section">
                <h3 @click="showBus=!showBus">
                    <i v-show="!showBus" class="fas fa-chevron-down"></i>
                    <i v-show="showBus" class="fas fa-chevron-up"></i>
                    Bottom Panel- Bus
                </h3>
                <div v-show="showBus">
                    <p>When a bus is selected, the bottom panel will show information relevant to that bus</p>
                    <p>If it is a converted electric bus, this panel will show two chargs: one representing the amount of miles the bus has driven over the course of the day, and one representing the bus's charge status throughought the day</p>
                    <p>If the bus is not converted in the selected plan, it will show only the miles driven chart </p>
                </div>
            </div>

            <div class="section">
                <h3 @click="showStation=!showStation">
                    <i v-show="!showStation" class="fas fa-chevron-down"></i>
                    <i v-show="showStation" class="fas fa-chevron-up"></i>
                    Bottom Panel- Station
                </h3>
                <div v-show="showStation">
                    <p>When a charging station is selected, the bottom panel will show information relevant to that station</p>
                    <p>Information includes UTA stop number, the list of buses currently at the station, and the current power output (at this point just the number of buses currently at station)</p>
                    <p>The chart to the left shows the number of buses at the station throughout the day</p>
                </div>
            </div>

            <div class="section">
                <h3 @click="showPlan=!showPlan">
                    <i v-show="!showPlan" class="fas fa-chevron-down"></i>
                    <i v-show="showPlan" class="fas fa-chevron-up"></i>
                    Plan Details Panel
                </h3>
                <div v-show="showPlan">
                    <p>This panel shows all static data pertaining to the implementation plan.</p>
                    <p>Plan implementations can be switched using the drop down at the top, this will update the whole screen</p>
                    <p>Comparison features?</p>
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
