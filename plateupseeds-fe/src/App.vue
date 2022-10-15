<script lang="ts">
import Nav from "./components/Nav.vue";
import AccordianSeedType from "./components/AccordianSeedType.vue";
import CardModal from "./components/CardModal.vue";


export default {
  components: {
    Nav,
    AccordianSeedType,
    CardModal,
  },
  data() {
    return {
      userId: -1,
      userLoggedIn: false,
      showModal: false,
      seedName: "",
      seedId: -1,
    }
  },
  methods: {
    setUser(userId: number, userLoggedIn: boolean) {
      this.userId = userId;
      this.userLoggedIn = userLoggedIn;
    },
    showModalApp(seedName: string, seedId: number) {
      this.showModal = true;
      this.seedName = seedName;
      this.seedId = seedId;
    },
    hideModalApp() {
      this.showModal = false;
    },
  },
};
</script>

<template>
  <header>
    <div class="wrapper">
      <Nav @loggedIn="setUser" />
    </div>
  </header>

  <main>
    <div class="accordion">
      <AccordianSeedType seedType="large" title="Large Layouts" v-bind:userId=userId v-bind:userLoggedIn="userLoggedIn"
        @showModal="showModalApp" />
      <AccordianSeedType seedType="medium" title="Medium Layouts" v-bind:userId=userId v-bind:userLoggedIn="userLoggedIn"
        @showModal="showModalApp" />
      <AccordianSeedType seedType="small" title="Small Layouts" v-bind:userId=userId v-bind:userLoggedIn="userLoggedIn"
        @showModal="showModalApp" />
      <AccordianSeedType seedType="default" title="Default Layouts" v-bind:userId=userId v-bind:userLoggedIn="userLoggedIn"
        @showModal="showModalApp" />
    </div>
    <CardModal class="modal-sm" v-bind:showModal="showModal" v-bind:seedName="seedName" v-bind:seedId="seedId"
      v-bind:userId="userId" v-bind:userLoggedIn="userLoggedIn" @hideModal="hideModalApp"/>
  </main>
</template>
