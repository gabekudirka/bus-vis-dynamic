<template>
  <div class="underline" >
    <div class="routeName"
        @click="selectBus(route.busses[0])"
    > {{route.lineAbbr}}: {{ route.lineName }} </div>
    <ul v-if="(selected == true)">
        <li v-for="bus in route.busses"
            :key="bus"
            :class="['busName', (bus === chosenBus) ? 'activeBus' : '']"
            @click="selectBus(bus)"
        >
           {{ bus }}
        </li>
    </ul>
  </div>
</template>

<script>

export default {
    name: 'RouteItem',
    props: {
        id: {
            type: Number,
            required: true
        },
        route: {
            type: Object,
            required: true
        },
        selected: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            chosenBus: this.route.busses[0]
        };
    },
    methods: {
        selectBus(busNum) {
            this.chosenBus = busNum;
            if (this.$store.state.selectedRoute !== this.route.lineAbbr) {
                this.$store.dispatch('changeRoute', this.route.lineAbbr);
            }
            this.$store.dispatch('changeBus', busNum);
        },
     }

};

</script>

<style>
.underline{
    border-bottom: 1px solid grey;
}
.routeName{
    text-align: left;
    padding: 0.3em;
}
.busName{
    padding: 0.1em;
    padding-left: 2em;
    text-align:left;
}
.activeBus{
    color: red;
}

</style>
