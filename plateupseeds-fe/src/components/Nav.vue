<script lang="ts">
export default {
  methods: {
    onSignIn(googleUser) {
      var profile = googleUser.getBasicProfile();
      console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
      console.log('Name: ' + profile.getName());
      console.log('Image URL: ' + profile.getImageUrl());
      console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
    },
    signOut() {
      var auth2 = gapi.auth2.getAuthInstance();
      auth2.signOut().then(function () {
        console.log('User signed out.');
      });
    }
  }
}
</script>
<template>
  <nav class="navbar navbar-expand-lg bg-dark bg-opacity-75 rounded-bottom border navbar-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img src="../assets/favicon.png" alt="Logo" width="auto" height="100%" class="d-inline-block align-text-middle">
        PlateUp! Seeds
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" target="_blank" href="https://wiki.plateupgame.com/">Wiki</a>
          </li>
          <li class="nav-item">
            <div class="g-signin2" data-onsuccess="onSignIn"></div>
          </li>
          <li class="nav-item">
            <a href="#" onclick="signOut">Sign out</a>
          </li>
        </ul>
        <a href="https://www.buymeacoffee.com/dxyao" target="_blank">
          <button type="button" class="btn btn-warning" data-bs-toggle="tooltip" data-bs-placement="left"
            data-bs-title="This could be an ad, but nobody likes those. Consider donating instead!">
            <i class="bi bi-cup-hot"></i>
            Buy me a coffee?
          </button>
        </a>
      </div>
    </div>
  </nav>
</template>
