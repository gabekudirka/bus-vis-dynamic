import { createStore } from 'vuex';

export default createStore({
    state: {
        plan: 'p20',
        selectedBus: '1025',
        selectedRoute: '2X',
        selectedChargingStation: 22256
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
        }

    }
  });
