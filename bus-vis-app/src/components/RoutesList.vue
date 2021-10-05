<template>
  <div>
    <ul id="routeList">
        <li v-for="(item, i) in routeItems" :key="i">
            <RouteItem
                :id="i"
                :route="item"
                :selected="i === selectedRoute"
                @clicked="onClickRoute"
            />
        </li>
    </ul>
  </div>
</template>

<script>
import RouteItem from './RouteItem.vue';
import routes from '../data/allRoutes.json';

export default {
    name: 'RoutesList',
    components: {
        RouteItem,
    },
    props: {
        plan: {
            type: String,
            required: true
        },
    },
    data() {
        return {
            routeItems: routes,
            selectedRoute: 0,
            selectedBus: null
        };
    },
    // computed: {
    //     routeItems: function() {
    //         console.log(this.convJson(routes));
    //         return this.convJson(routes);
    //     },
    // },
     methods: {
        onClickRoute(value) {
            console.log('click route');
            console.log(value);
            if (this.selectedRoute !== value.routeID) {
                this.selectedRoute = value.routeID;
            }
            this.selectedBus = value.busNo;
        },
        // selectItem(i) {
        //     if (this.selectedRoute !== i) {
        //         console.log('changing');
        //         this.selectedRoute = i;
        //     }
        //     console.log(this.routeItems[i]);
        //     console.log(this.routeItems[i].busses[0]);
        // },
     }
};

</script>

<style>
#routeList{
    overflow-x: hidden;
    overflow-y: auto;
}
/* div.container {
  max-width: 80%;
} */

</style>
