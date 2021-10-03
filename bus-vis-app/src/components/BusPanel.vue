/* eslint-disable max-len */
<template>
<div class="container bottom-panel-box">
    <div class="row absolute">
        <div class="col-4 border">
            <div class="row border">
                text column
            </div>
        </div>
        <div class="col border">
            Graph column 1
        </div>
        <div class="col border">
            Graph column 2
        </div>
      </div>
</div>
</template>

<script>

export default {
  name: 'BusPanel',
};

</script>

<style>
div.container {
    max-width: 100%;
}

div.absolute {
    width: 100%;
    position: absolute;
    height: 100%;
}

div.bottom-panel-box {
    position: fixed;
    height: 350px;
    border-top: 3px solid;
    bottom: 0px;
}
</style>
