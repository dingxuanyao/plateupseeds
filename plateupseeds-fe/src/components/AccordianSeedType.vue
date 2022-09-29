<script lang="ts">
import CardSeed from "./CardSeed.vue";
const API_URL = `http://localhost:8000`;
export default {
  components: {
    CardSeed,
  },
  props: {
    seedType: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
  },
  created() {
    // fetch on init
    this.fetchSeeds();
  },
  data() {
    return {
      seeds: [],
      // TODO: hardcoded for now
      userId: 2,
    }
  },
  methods: {
    fetchSeeds() {
      fetch(`${API_URL}/seeds_by_type/${this.seedType}`)
        .then((response) => response.json())
        .then((data) => {
          this.seeds = data
        })
    },
  },
};
</script>

<template>
  <div class="accordion-item border-bottom-1 border-secondary">
    <h2 class="accordion-header">
      <button class="accordion-button collapsed bg-dark text-white" type="button" data-bs-toggle="collapse"
        v-bind:data-bs-target="`.${seedType}`">
        <h2>{{ title }}</h2>
      </button>
    </h2>
    <!-- <div class="row m-0 bg-dark" id="seed-large-preview"></div> -->
    <div class="accordion-collapse collapse" v-bind:class="seedType">
      <div class="row m-0 bg-dark" v-bind:id="`seed-${seedType}`">
        <CardSeed v-for="seed in seeds" v-bind:seedId="seed.id" v-bind:seedName="seed.seed_name" v-bind:userId="userId" />
      </div>
    </div>
  </div>
</template>
