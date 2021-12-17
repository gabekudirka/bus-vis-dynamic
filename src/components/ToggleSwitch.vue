<template>
  <div class="toggle-switch">
    <button
        class="button toggle"
        @click="toggle"
        :class="[!showBusses ? 'active' : '']"
    >Stations</button>
    <button
        class="button toggle"
        @click="toggle"
        :class="[showBusses ? 'active' : '']"
    >Buses</button>
    </div>
</template>

<script>

export default {
    name: 'ToggleSwitch',
    props: {
        initShowBusses: {
            type: Boolean,
            default: true
        }
    },
    data() {
        return {
            showBusses: this.initShowBusses,
        };
    },
    computed: {
        showBussesState: function () {
            return this.$store.state.showBusses;
        }
    },
    watch: {
        showBussesState: function () {
            this.changeToggle();
        }
    },
    methods: {
       toggle() {
            this.$store.dispatch('changeShowBusses', !this.showBusses);
        },
        changeToggle() {
            this.showBusses = !this.showBusses;
        }
    },
};

</script>

<style>
.toggle-switch{
    margin:1em;
}
.toggle {
    padding: 2px 6px ;
}
.toggle-switch > .toggle:first-of-type {
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}
.toggle-switch > .toggle:last-of-type {
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}
button{
    border: 1.5px solid lightseagreen;
    color: lightseagreen;
}
.active{
    background-color: lightseagreen;
    color: white;
}

/* div.container {
  max-width: 80%;
} */

</style>
