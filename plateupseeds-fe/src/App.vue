<script lang="ts">
import Nav from "./components/Nav.vue";
import AccordianSeedType from "./components/AccordianSeedType.vue";
import AccordianQAndA from "./components/AccordianQAndA.vue";
import CardModal from "./components/CardModal.vue";



export default {
  components: {
    Nav,
    AccordianSeedType,
    CardModal,
    AccordianQAndA,
  },
  data() {
    return {
      userId: -1,
      userAnonymousName: '',
      userLoggedIn: false,
      showModal: false,
      seedName: "",
      seedId: -1,
    }
  },
  methods: {
    setUser(userId: number, userAnonymousName: string, userLoggedIn: boolean) {
      this.userId = userId;
      this.userLoggedIn = userLoggedIn;
      this.userAnonymousName = userAnonymousName;
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
  <div class="container-lg">
    <header>
      <div class="wrapper">
        <Nav @loggedIn="setUser" />
      </div>
    </header>

    <main>
      <div class="accordion">
        <AccordianSeedType seedType="large" title="Large Layouts" v-bind:userId=userId
          v-bind:userLoggedIn="userLoggedIn" @showModal="showModalApp" />
        <AccordianSeedType seedType="medium" title="Medium Layouts" v-bind:userId=userId
          v-bind:userLoggedIn="userLoggedIn" @showModal="showModalApp" />
        <AccordianSeedType seedType="small" title="Small Layouts" v-bind:userId=userId
          v-bind:userLoggedIn="userLoggedIn" @showModal="showModalApp" />
        <AccordianSeedType seedType="default" title="Default Layouts" v-bind:userId=userId
          v-bind:userLoggedIn="userLoggedIn" @showModal="showModalApp" />
        <AccordianQAndA seedType="default" title="FAQ" v-bind:userId=userId
          v-bind:userLoggedIn="userLoggedIn" @showModal="showModalApp" />
      </div>
      <CardModal class="modal-sm" v-bind:showModal="showModal" v-bind:seedName="seedName" v-bind:seedId="seedId"
        v-bind:userId="userId" v-bind:userLoggedIn="userLoggedIn" @hideModal="hideModalApp" />
    </main>
  </div>
</template>
<style>
/* background dark green */
body {
  background-color: #1a1a1a;
}

.accordion-button.collapsed::after {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23fff'%3e%3cpath fill-rule='evenodd' d='M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z'/%3e%3c/svg%3e");
}
</style>
