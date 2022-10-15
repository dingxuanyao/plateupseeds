<script lang="ts">
import CardSeed from "./CardSeed.vue";
import ReloadIcon from "./icons/ReloadIcon.vue";
import CloseIcon from "./icons/CloseIcon.vue";
import { defineComponent } from 'vue'
const API_URL = import.meta.env.VITE_API_URL;
const SEEDS_PER_PAGE = 18;
export default defineComponent({
  components: {
    CardSeed,
    ReloadIcon,
    CloseIcon,
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
    userId: {
      type: Number,
      required: true,
    },
    userLoggedIn: {
      type: Boolean,
      required: true,
    },
  },
  created() {
    // fetch on init
    this.fetchSeeds();
    this.fetchNumPages();
  },
  data() {
    return {
      seeds: [],
      currentPage: 1,
      totalPages: 1,
      pageRange: [],
      random: false,
    }
  },
  watch: {
    currentPage: function (newPage, oldPage) {
      this.fetchSeeds();
      this.updatePageRange();
    },
    totalPages: function (newPage, oldPage) {
      this.updatePageRange();
    },
  },
  methods: {
    fetchSeeds() {
      fetch(`${API_URL}/seeds_by_type/${this.seedType}?limit=${SEEDS_PER_PAGE}&skip=${(this.currentPage - 1) * SEEDS_PER_PAGE}&random=${this.random}`)
        .then((response) => response.json())
        .then((data) => {
          this.seeds = data
        })
    },
    fetchNumPages() {
      fetch(`${API_URL}/count_seeds_by_type/${this.seedType}`)
        .then((response) => response.json())
        .then((data) => {
          this.totalPages = Math.ceil(data / SEEDS_PER_PAGE);
        })
    },
    updatePageRange() {
      const pages = [];
      const numberToRender = 5;
      for (let i = 1; i <= this.totalPages; i++) {
        if (Math.abs(this.currentPage - i) <= numberToRender) {
          pages.push(i);
        }
      }
      this.pageRange = pages;
    },
    changePage(page: number) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    showModal(seedName: string, seedId: number) {
      this.$emit('showModal', seedName, seedId);
    },
    randomize() {
      this.random = true;
      this.fetchSeeds();
    },
    disableRandom() {
      this.random = false;
      this.fetchSeeds();
    },
  },
  emits: ['showModal'],
});
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
      <div class="row p-3 bg-dark">
        <div>
          <button class="btn btn-success" v-bind:class="random ? null : 'bg-transparent'" @click="randomize">
            <ReloadIcon></ReloadIcon>
            random
          </button>
          <button class="btn btn-danger bg-transparent" :disabled="!random" @click="disableRandom">
            <CloseIcon></CloseIcon>
          </button>
        </div>
      </div>
      <div class="row m-0 bg-dark" v-bind:id="`seed-${seedType}`">
        <CardSeed v-for="seed in seeds" v-bind:seedId="seed" v-bind:userId="userId" v-bind:userLoggedIn="userLoggedIn"
          @showModal=showModal />
        <nav>
          <ul class="pagination">
            <li class="page-item"><a class="page-link bg-dark border-secondary btn"
                @click="changePage(currentPage - 1)">Previous</a></li>
            <template v-for="page in this.pageRange">
              <li class="page-item"><a class="page-link bg-dark border-secondary btn" @click="changePage(page)"
                  v-bind:class="page==currentPage ? 'active' : null ">{{ page }}</a></li>
            </template>
            <li class="page-item"><a class="page-link bg-dark border-secondary btn"
                @click="changePage(currentPage + 1)">Next</a></li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>
