<script lang="ts">
const MEDIA_URL = `https://media.plateupseeds.com/seeds_sorted`;
export default {
  // data: () => ({
  //   showModal: false
  // }),
  props: {
    showModal: {
      type: Boolean,
      required: true
    },
    seedName: {
      type: String,
      // required: true,
    },
    seedType: {
      type: String,
      // required: true,
    },
    seedId: {
      type: Number,
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
      return `${MEDIA_URL}/high_quality/${seedName}.jpg`;
    },
    hideModal() {
      this.$emit('hideModal');
    }
  },
  emits: ['hideModal']
}
</script>
<template>
  <div>
    <vue-final-modal v-model="showModal" classes="modal-container" content-class="modal-content bg-dark text-white" @closed="hideModal">
      <span class="modal__title">{{seedName}}</span>
      <span class="modal__content">
        <img :src="getSeedUrlHighQuality(seedName)" style="width: 40vw;">
      </span>
    </vue-final-modal>
    <!-- <button @click="showModal = true">Open Modal</button> -->
  </div>
</template>
<style scoped>
::v-deep .modal-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: auto;
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
</style>
