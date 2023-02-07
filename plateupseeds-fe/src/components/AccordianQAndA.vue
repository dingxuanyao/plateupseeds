<script lang="ts">
import QAndAItem from "./QAndAItem.vue";
import { defineComponent } from 'vue'
const API_URL = import.meta.env.VITE_API_URL;
const SEEDS_PER_PAGE = 18;
export default defineComponent({
  components: {
    QAndAItem,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
  },
});
</script>

<template>
  <div class="accordion-item border-bottom-1 border-secondary">
    <h2 class="accordion-header">
      <button class="accordion-button show bg-dark text-white" type="button" data-bs-toggle="collapse"
        v-bind:data-bs-target="`.FAQ`">
        <h2>{{ title }}</h2>
      </button>
    </h2>
    <div class="accordion-collapse show bg-dark text-white" v-bind:class="`FAQ`">
      <QAndAItem question="None of the large maps, or even medium maps are showing up for me"
        answer="Floorplan sizes and floorplan themes are unlocked by levelling up. Check out the official <a class='link-light' href='https://wiki.plateupgame.com/ExperienceLevels' target='_blank'>plateup wiki</a> for details." />
      <QAndAItem question="Why does the seed from here not match the seed in my game?"
        answer="This is a known bug. Close and restart your game and try again. If this still doesn't work, maybe 1) a typo in the seed, or a new game update scrambled all the seeds (this site currently posts seeds from v1.1.2)" />
      <QAndAItem question="Why are there no North Pole seeds?"
        answer="North Pole maps are not currently available as seeded runs. The developers are working on a system to toggle the seasonal events on and off outside of their perspective holidays but it's not ready yet." />
    </div>
  </div>
</template>
