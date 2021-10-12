import { createStore } from 'vuex';

export default createStore({
    state: {
        plan: 'p20',
        selectedBus: '1025',
        selectedRoute: '2X',
        selectedChargingStation: 22256,
        time: '4:00'
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
            state.selectedChargingStation = stationId;
        },
        CHANGE_TIME(state, time) {
            state.time = time;
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
            commit('CHANGE_SELECTED_STATION', payload);
        },
        changeTime({ commit }, payload) {
            commit('CHANGE_TIME', payload);
        },

    }
  });
