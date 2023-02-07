<script lang="ts">
import Comments from "./Comments.vue";

const MEDIA_URL = `https://media.plateupseeds.com`;
export default {
  components: {
    Comments,
  },
  props: {
    showModal: {
      type: Boolean,
      required: true
    },
    seedName: {
      type: String,
      default: ""
      // required: true,
    },
    seedType: {
      type: String,
      // required: true,
    },
    seedId: {
      type: Number,
      default: -1
      // required: true,
    },
    userId: {
      type: Number,
      // required: true,
    },
    userLoggedIn: {
      type: Boolean,
      // required: true,
    },
  },
  methods: {
    getSeedUrlHighQuality(seedName: string) {
      return `${MEDIA_URL}/v1.1.2/${seedName}_original.jpg`;
    },
    hideModal() {
      this.$emit('hideViewSeedModal');
    }
  },
  emits: ['hideViewSeedModal']
}
</script>
<template>
  <div>
    <vue-final-modal v-model="showModal" classes="modal-container" content-class="modal-content bg-dark text-white"
      @closed="hideModal" :esc-to-close=true>
      <span class="modal__title">{{seedName}}</span>
      <span class="modal__content">
        <img :src="getSeedUrlHighQuality(seedName)">
        <Comments v-bind:seedId="seedId" v-bind:userId="userId"></Comments>
      </span>
    </vue-final-modal>
  </div>
</template>
<style scoped>
::v-deep .modal-container {
  display: flex;
  justify-content: center;
  align-items: start;
  width: 100vw;
  overflow: scroll;
}

::v-deep .modal-content {
  display: flex;
  flex-direction: column;
  margin: 0 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  background: #fff;
  width: auto;
}

.modal__title {
  font-size: 1.5rem;
  font-weight: 700;
}

img {
  width: 40vw;
  display: block;
  margin: 0 auto;
  height: auto;
}
</style>
