import { createStore } from 'vuex';

export default createStore({
    state: {
        plan: 'p20',
        selectedBus: '1026',
        selectedRoute: '45',
        selectedChargingStation: '7'
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
            state.selectedRoute = routeId;
        },
        CHANGE_SELECTED_CHARGING_STATION(state, stationId) {
            state.selectedChargingStation = stationId;
        },
    },
    actions: {
        changeBus({ commit }, payload) {
            commit('CHANGE_SELECTED_BUS', payload);
        }
    }
  });
