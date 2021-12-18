<template>
  <div>
    <ul id="routeList">
        <li v-for="(item, i) in routeItems" :key="item.lineAbbr">
            <RouteItem
                :id="i"
                :route="item"
                :selected="item.lineAbbr === selectedRoute"
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
    data() {
        return {
            routeItems: routes,
        };
    },
    computed: {
        plan: function () {
            return this.$store.state.plan;
        },
        selectedRoute: function () {
            return this.$store.state.selectedRoute;
        }
    },
};

</script>

<style>
#routeList{
    overflow-x: hidden;
    overflow-y: auto;
}
ul#routeList > li:nth-of-type(odd) {
    background-color: white;
}
/* div.container {
  max-width: 80%;
} */

</style>
