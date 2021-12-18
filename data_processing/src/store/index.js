import { createStore } from 'vuex';

export default createStore({
    state: {
        plan: 'p20',
        selectedBus: '1025',
        selectedRoute: '2X',
        selectedChargingStation: '7',
        time: '01:40',
        showBusses: true,
        routeFocused: false,
        routeFocusedNum: -1,
        bussesToShow: null,
        busLocations: {
            type: 'FeatureCollection',
            features: [{
                type: 'Feature',
                properties: { 
                    id: -1,
                    converted: 0,
                    atStation: true,
                    remainingCharge: 100,
                    show: true
                },
                geometry: {
                    type: 'Point',
                    coordinates: [0, 0]
                }
            }]
        },
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
        CHANGE_TIME(state, time) {
            state.time = time;
        },
        CHANGE_SHOW_BUSSES(state, showBusses) {
            state.showBusses = showBusses;
        },
        CHANGE_BUS_LOCATIONS(state, busLocations) {
            state.busLocations = busLocations;
        },
        CHANGE_BUSESS_TO_SHOW(state, bussesToShow) {
            state.bussesToShow = bussesToShow;
        },
        CHANGE_ROUTE_FOCUSED(state, routeFocused) {
            state.routeFocused = routeFocused;
        },
        CHANGE_ROUTE_FOCUSED_NUM(state, routeFocusedNum) {
            console.log(routeFocusedNum);
            state.routeFocusedNum = routeFocusedNum;
        }
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
            commit('CHANGE_BUS_LOCATIONS', payload);
        },
        changeBussesToShow({ commit }, payload) {
            commit('CHANGE_BUSESS_TO_SHOW', payload);
        },
        changeRouteFocused({ commit }, payload) {
            commit('CHANGE_ROUTE_FOCUSED', payload);
        },
        changeRouteFocusedNum({ commit }, payload) {
            commit('CHANGE_ROUTE_FOCUSED_NUM', payload);
        }
    }
  });
