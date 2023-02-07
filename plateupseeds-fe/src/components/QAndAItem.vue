<script lang="ts">
import { defineComponent } from 'vue'
const API_URL = import.meta.env.VITE_API_URL;
const SEEDS_PER_PAGE = 18;
export default defineComponent({
  props: {
    question: {
      type: String,
      required: true,
    },
    answer: {
      type: String,
      required: true,
    },
  },
});
</script>

<template>
  <div class="row m-0">
    <h3 class="col-12 mt-3">{{ question }}</h3>
    <p class="col-12 mb-3" v-html="answer"></p>
  </div>
</template>
  