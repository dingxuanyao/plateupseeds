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
      pageRange: [0], // how to typescript this?
      random: false,
      sortByLikes: true,
      filterByTheme: 'all',
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
    sortByLikes: function (newSort, oldSort) {
      this.fetchSeeds();
      this.updatePageRange();
    },
    filterByTheme: function (newTheme, oldTheme) {
      this.fetchSeeds();
      this.updatePageRange();
    },
  },
  methods: {
    fetchSeeds() {
      fetch(`${API_URL}/seeds_by_type/${this.seedType}?limit=${SEEDS_PER_PAGE}&skip=${(this.currentPage - 1) * SEEDS_PER_PAGE}&random=${this.random}&sort_by_likes=${this.sortByLikes}&seed_theme=${this.filterByTheme}`)
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
    pass() {
      return;
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
    <div class="accordion-collapse collapse" v-bind:class="seedType">
      <div class="p-3 bg-dark">
        <div class="btn-group me-3">
          <button type="button" class="btn btn-success" v-bind:class="random ? null : 'bg-transparent'"
            @click="randomize">
            <ReloadIcon></ReloadIcon>
            random
          </button>
          <button type="button" class="btn btn-danger bg-transparent" :disabled="!random" @click="disableRandom">
            <CloseIcon></CloseIcon>
          </button>
        </div>
        <div class="btn-group me-3">
          <input type="radio" class="btn-check" v-bind:value=true v-bind:name="`btngroup-sortByLikes-${seedType}`" v-bind:id="`likesSelected-${seedType}`" v-model="sortByLikes" checked>
          <label class="btn btn-outline-success" v-bind:for="`likesSelected-${seedType}`">Likes</label>
          <input type="radio" class="btn-check" v-bind:value=false v-bind:name="`btngroup-sortByLikes-${seedType}`" v-bind:id="`commentsSelected-${seedType}`" v-model="sortByLikes">
          <label class="btn btn-outline-success" v-bind:for="`commentsSelected-${seedType}`">Comments</label>
        </div>
        <div class="btn-group me-3">
          <input type="radio" class="btn-check" v-bind:value="`all`" v-bind:name="`btngroup-filterAllThemes-${seedType}`" v-bind:id="`filterAllThemes-${seedType}`" v-model="filterByTheme" checked>
          <label class="btn btn-outline-success" v-bind:for="`filterAllThemes-${seedType}`">All</label>
          <input type="radio" class="btn-check" v-bind:value="`COUNTRY`" v-bind:name="`btngroup-filterCountryThemes-${seedType}`" v-bind:id="`filterCountryThemes-${seedType}`" v-model="filterByTheme">
          <label class="btn btn-outline-success" v-bind:for="`filterCountryThemes-${seedType}`">COUNTRY</label>
          <input type="radio" class="btn-check" v-bind:value="`ALPINE`" v-bind:name="`btngroup-filterAlpineThemes-${seedType}`" v-bind:id="`filterAlpineThemes-${seedType}`" v-model="filterByTheme">
          <label class="btn btn-outline-success" v-bind:for="`filterAlpineThemes-${seedType}`">ALPINE</label>
          <input type="radio" class="btn-check" v-bind:value="`CITY`" v-bind:name="`btngroup-filterCityThemes-${seedType}`" v-bind:id="`filterCityThemes-${seedType}`" v-model="filterByTheme">
          <label class="btn btn-outline-success" v-bind:for="`filterCityThemes-${seedType}`">CITY</label>
          <input type="radio" class="btn-check" v-bind:value="`AUTUMN`" v-bind:name="`btngroup-filterAutumnThemes-${seedType}`" v-bind:id="`filterAutumnThemes-${seedType}`" v-model="filterByTheme">
          <label class="btn btn-outline-success" v-bind:for="`filterAutumnThemes-${seedType}`">AUTUMN</label>
        </div>
      </div>
      <div class="row m-0 bg-dark" v-bind:id="`seed-${seedType}`">
        <CardSeed v-for="seed in seeds" v-bind:seedId="seed" v-bind:userId="userId" v-bind:userLoggedIn="userLoggedIn"
          @showModal=showModal />
        <nav>
          <ul class="pagination">
            <li class="page-item"><a class="page-link bg-dark border-secondary btn"
                @click="changePage(currentPage - 1)">Previous</a></li>
            <template v-for="page in pageRange">
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
