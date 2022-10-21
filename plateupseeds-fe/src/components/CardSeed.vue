<script lang="ts">
import ThumbsUp from "./icons/ThumbsUp.vue";
import ThumbsDown from "./icons/ThumbsDown.vue";
import CommentsIcon from "./icons/CommentsIcon.vue";
const API_URL = import.meta.env.VITE_API_URL;
const MEDIA_URL = `https://media.plateupseeds.com/seeds_sorted`;
import { defineComponent } from 'vue'

export default defineComponent({
  components: {
    ThumbsUp,
    ThumbsDown,
    CommentsIcon,
  },
  props: {
    // seedName: {
    //   type: String,
    //   required: true,
    // },
    // seedType: {
    //   type: String,
    //   required: true,
    // },
    seedId: {
      type: Number,
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
    // likes: {
    //   type: [Object],
    //   required: true,
    // },
  },
  watch: {
    userId: function (newUserId, oldUserId) {
      this.fetchLikes();
    },
    seedId: function (newSeedId, oldSeedId) {
      this.fetchLikes();
    },
  },
  data() {
    return {
      seedName: "",
      seedType: "",
      likes: [],
      dislikes: [],
      userLiked: false,
      userDisliked: false,
      comments: [],
    }
  },
  computed: {
    // numLikes() {
    //   return this.likes.likes.length;
    // },
    // numDislikes() {
    //   return this.likes.dislikes.length;
    // },
  },
  created() {
    this.fetchLikes();
  },
  methods: {
    buttonClass(likeButton: boolean) {
      var classString = "";
      if (likeButton && !this.userLiked) {
        classString += 'bg-transparent ';
      } else if (!likeButton && !this.userDisliked) {
        classString += 'bg-transparent ';
      }
      if (!this.userLoggedIn) {
        classString += 'disabled';
      }
      return classString;
    },
    fetchLikes() {
      fetch(`${API_URL}/seeds/${this.seedId}`)
        .then((response) => response.json())
        .then((data) => {
          this.seedName = data.seed_name;
          this.seedType = data.seed_type;
          this.likes = data.likes.filter((like: any) => like.is_like);
          this.dislikes = data.likes.filter((like: any) => !like.is_like);
          this.userLiked = this.likes.filter((like: any) => like.user_id === this.userId).length > 0;
          this.userDisliked = this.dislikes.filter((like: any) => like.user_id === this.userId).length > 0;
          this.comments = data.comments;
        })
    },
    getSeedUrl(seedName: string, seedType: string) {
      return `${MEDIA_URL}/${seedType}/${seedName}.jpg`;
    },
    getSeedUrlHighQuality(seedName: string) {
      return `${MEDIA_URL}/high_quality/${seedName}.jpg`;
    },
    toggle(isLikedButton: boolean) {
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
    showModal() {
      this.$emit('showModal', this.seedName, this.seedId);
    },
  },
  emits: ['showModal'],
});
</script>

<template>
  <div class="col-lg-2 col-sm-4 p-0">
    <div class="card text-white bg-dark text-center border-secondary m-0"
      v-bind:data-bs-photourl="getSeedUrl(seedName, seedType)">
      <div class="card-body">
        <div>
          <img v-bind:src="getSeedUrl(seedName, seedType)" class="card-img-top btn p-0" alt="Responsive image"
            loading="lazy" @click="showModal" />
        </div>
        <div class="card-text">{{ seedName }}</div>
        <div class="text-start">
          <button class="btn btn-success" v-bind:class="buttonClass(true)" @click="toggle(true)">
            <ThumbsUp />
            {{ likes.length }}
          </button>
          <button class="btn btn-danger" v-bind:class="buttonClass(false)" @click="toggle(false)">
            <ThumbsDown />
            {{ dislikes.length }}
          </button>
          <button class="btn btn-secondary bg-transparent" @click="showModal">
            <CommentsIcon />
            {{ comments.length }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
img:hover {
  /* border: 5px; */
  border-style: solid;
  border-color: #007bff;
}
</style>
