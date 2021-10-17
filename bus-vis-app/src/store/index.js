import { createStore } from 'vuex';

export default createStore({
    state: {
        plan: 'p60',
        selectedBus: '1025',
        selectedRoute: '2X',
        selectedChargingStation: '7',
        time: '12:20',
        showBusses: true,
        busLocations: []
    },
    getters: {},
    mutations: {
        CHANGE_PLAN(state, plan) {
            state.plan = plan;
        },
        CHANGE_SELECTED_BUS(state, busId) {
            state.selectedBus = busId;
        },
        CHANGE_SELECTED_ROUTE(state, routeId) {
            console.log(routeId);
            state.selectedRoute = routeId;
        },
        CHANGE_SELECTED_CHARGING_STATION(state, stationId) {
            console.log('setting', stationId);
            state.selectedChargingStation = stationId;
        },
        CHANGE_TIME(state, time) {
            state.time = time;
        },
        CHANGE_SHOW_BUSSES(state, showBusses) {
            state.showBusses = showBusses;
        },
        CHANGE_BUS_LOCATIONS(state, busLocations) {
            state.busLocations = busLocations;
        },
    },
    actions: {
        changePlan({ commit }, payload) {
            commit('CHANGE_PLAN', payload);
        },
        changeRoute({ commit }, payload) {
            commit('CHANGE_SELECTED_ROUTE', payload);
        },
        changeBus({ commit }, payload) {
            commit('CHANGE_SELECTED_BUS', payload);
        },
        changeStation({ commit }, payload) {
            commit('CHANGE_SELECTED_CHARGING_STATION', payload);
        },
        changeTime({ commit }, payload) {
            commit('CHANGE_TIME', payload);
        },
        changeShowBusses({ commit }, payload) {
            commit('CHANGE_SHOW_BUSSES', payload);
        },
        changeBusLocations({ commit }, payload) {
            console.log('changebuslocs', payload[0]);
            commit('CHANGE_BUS_LOCATIONS', payload);
        },

    }
  });
