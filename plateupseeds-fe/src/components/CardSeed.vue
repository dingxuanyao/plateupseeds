<script lang="ts">
import ThumbsUp from "./icons/ThumbsUp.vue";
import ThumbsDown from "./icons/ThumbsDown.vue";
const API_URL = `http://localhost:8000`;
const ASSETS_URL = `https://plateupseeds.com/seeds_sorted/high_quality`;

export default {
  components: {
    ThumbsUp,
    ThumbsDown
  },
  props: {
    seedName: {
      type: String,
      required: true,
    },
    seedId: {
      type: Number,
      required: true,
    },
    userId: {
      type: Number,
      required: true,
    },
  },
  created() {
    // fetch on init
    this.fetchLikes();
  },
  data() {
    return {
      likes: [],
      dislikes: [],
      userLiked: false,
      userDisliked: false,
    }
  },
  methods: {
    fetchLikes() {
      fetch(`${API_URL}/likes/${this.seedName}`)
        .then((response) => response.json())
        .then((data) => {
          this.likes = data.filter((like) => like.is_like).map((like) => like.user_id);
          this.dislikes = data.filter((like) => !like.is_like).map((like) => like.user_id);
          this.userLiked = this.likes.includes(this.userId);
          this.userDisliked = this.dislikes.includes(this.userId);
        })
    },
    getSeedUrl(seedName: string) {
      return `${ASSETS_URL}/${seedName}.jpg`;
    },
    toggle(isLikedButton: boolean) {
      // console.log("isLikedButton" + isLikedButton);
      // console.log("userLiked" + this.userLiked);
      if (isLikedButton && this.userLiked) {
        this.deleteLike();
      } else if (!isLikedButton && this.userDisliked) {
        this.deleteLike();
      } else {
        this.updateLike(isLikedButton);
      }
    },
    deleteLike() {
      fetch(`${API_URL}/likes/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: this.userId,
          seed_id: this.seedId,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.fetchLikes();
        });
    },
    updateLike(isLikedButton: boolean) {
      fetch(`${API_URL}/likes/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: this.userId,
          seed_id: this.seedId,
          is_like: isLikedButton,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.fetchLikes();
        });
    },
  },
};
</script>

<template>
  <div class="col-lg-2 col-sm-4 p-0">
    <div class="card text-white bg-dark text-center border-secondary m-1" v-bind:data-bs-photourl=getSeedUrl(seedName)>
      <div class="card-body">
        <div style="width:100%;height:0; padding-top:80%;position:relative;">
          <img v-bind:src=getSeedUrl(seedName) class="card-img-top btn" alt="Responsive image" loading="lazy"
            data-bs-toggle="modal" data-bs-target="#exampleModal"
            style="position:absolute; top:0; left:0; width:100%;" />
        </div>
        <div class="card-text">{{ seedName }}</div>
        <div class="text-start">
          <button class="btn btn-success" v-bind:class="userLiked ? null : 'bg-transparent'" @click="toggle(like=true)">
            <ThumbsUp />
            {{ likes.length }}
          </button>
          <button class="btn btn-danger" v-bind:class="userDisliked ? null : 'bg-transparent'" @click="toggle(like=false)">
            <ThumbsDown />
            {{ dislikes.length }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
