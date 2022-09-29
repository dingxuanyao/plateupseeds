<script lang="ts">
import Nav from "./components/Nav.vue";
// import TheWelcome from "./components/TheWelcome.vue";
import AccordianSeedType from "./components/AccordianSeedType.vue";
// import TheWelcome from "./components/TheWelcome.vue";
// import App from "./components/App.vue";

export default {
  components: {
    Nav,
    AccordianSeedType,
  },
};
</script>

<template>
  <header>
    <div class="wrapper">
      <Nav />
    </div>
  </header>

  <main>
    <div class="accordion">
      <AccordianSeedType seedType="large" title="Large Layouts" />
      <AccordianSeedType seedType="medium" title="Medium Layouts" />
      <AccordianSeedType seedType="small" title="Small Layouts" />
      <AccordianSeedType seedType="default" title="Default Layouts" />
    </div>
  </main>
</template>
