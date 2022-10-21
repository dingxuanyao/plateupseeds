<script lang="ts">
import { defineComponent } from 'vue'
const API_URL = import.meta.env.VITE_API_URL;

const dayToString = (day: number) => {
  switch (day) {
    case 0:
      return "Sun";
    case 1:
      return "Mon";
    case 2:
      return "Tues";
    case 3:
      return "Wed";
    case 4:
      return "Thu";
    case 5:
      return "Fri";
    case 6:
      return "Sat";
  }
}

const monthToStr = (month: number) => {
  switch (month) {
    case 0:
      return "Jan";
    case 1:
      return "Feb";
    case 2:
      return "Mar";
    case 3:
      return "Apr";
    case 4:
      return "May";
    case 5:
      return "Jun";
    case 6:
      return "Jul";
    case 7:
      return "Aug";
    case 8:
      return "Sep";
    case 9:
      return "Oct";
    case 10:
      return "Nov";
    case 11:
      return "Dec";
  }
}

export default defineComponent({
  props: {
    seedId: {
      type: Number,
      required: true,
    },
    userId: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    comments: [],
    new_comment: "",
    username: "",
    new_username: "",
    email: "",
  }),
  watch: {
    seedId: function (newSeedId, oldSeedId) {
      this.fetchComments();
    },
    userId: function (newUserId, oldUserId) {
      this.updateUsername();
    },
  },
  created() {
    this.fetchComments();
    this.updateUsername();
  },
  methods: {
    parseMinutes: function (minutes: number) {
      if (minutes < 10) {
        return "0" + minutes;
      }
      return minutes;
    },
    parseDatetime(datetime: string) {
      const date = new Date(datetime);
      const now = new Date()
      const diff = now.getTime() - date.getTime();
      const offset = date.getTimezoneOffset() * 60 * 1000;
      const dateWithOffset = new Date(date.getTime() - offset);


      var month = monthToStr(dateWithOffset.getMonth());
      var dateNum = dateWithOffset.getDate();
      var year = dateWithOffset.getFullYear();
      var day = dayToString(dateWithOffset.getDay());
      var am = dateWithOffset.getHours() < 12 ? "AM" : "PM";
      var hours = am == "AM" ? String(dateWithOffset.getHours()) : String(dateWithOffset.getHours() - 12);
      var minutes = this.parseMinutes(dateWithOffset.getMinutes());

      // still today
      if (dateWithOffset.getDate() === now.getDate()) {
        return `${hours}:${minutes} ${am}`;
      }
      // This week
      else if (diff < 7 * 24 * 60 * 60 * 1000) {
        return `${day} ${hours}:${minutes} ${am}`;
      }
      // this year
      else if (dateWithOffset.getFullYear() === now.getFullYear()) {
        return `${month} ${dateNum} ${hours}:${minutes} ${am}`;
      }
      else {
        return `${month} ${dateNum}, ${year}, ${hours}:${minutes} ${am}`;
      }
    },
    fetchComments() {
      this.comments = [];
      fetch(`${API_URL}/comments/${this.seedId}`)
        .then((response) => response.json())
        .then((data) => {
          for (let i = 0; i < data.length; i++) {
            fetch(`${API_URL}/users/${data[i].user_id}`)
              .then((response) => response.json())
              .then((user) => {
                let username = user.anonymous_name ? user.anonymous_name : user.email;
                let comment = {
                  id: data[i].id,
                  comment: data[i].comment,
                  created_time: this.parseDatetime(data[i].created_time),
                  username: username,
                };
                this.comments.push(comment);
              });
          }
        });
    },
    updateUsername() {
      fetch(`${API_URL}/users/${this.userId}`)
        .then((response) => response.json())
        .then((user) => {
          this.username = user.anonymous_name ? user.anonymous_name : user.email;
          this.new_username = this.username;
          this.email = user.email;
        });
    },
    updateAnonymousName() {
      fetch(`${API_URL}/users/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: this.userId,
          email: this.email,
          anonymous_name: this.new_username,
        }),
      });
    },
    submitComment() {
      if (this.new_comment === "") {
        return;
      }
      if (this.username !== this.new_username) {
        this.updateAnonymousName();
      }
      fetch(`${API_URL}/comments/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          seed_id: this.seedId,
          user_id: this.userId,
          comment: this.new_comment,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.fetchComments();
        });
    },
  },
});

</script>
<template>
  <div>
    <div class="flex flex-col">
      <div class="flex flex-row justify-between">
        <div>
          <form class="form-floating text-black">
            <input type="string" class="form-control" id="PostingAs" v-model="new_username">
            <label for="PostingAs">Posting as</label>
          </form>
        </div>
        <div>
          <div class="form-floating text-black">
            <textarea class="form-control" id="newComment" v-model="new_comment"></textarea>
            <label for="newComment">Tell us something about this seed!</label>
          </div>
        </div>
        <div>
          <button class="btn btn-success" :disabled="userId == -1" @click="submitComment">
            Add Comment
          </button>
        </div>
      </div>
      <div>
        <div v-for="comment in comments" :key="comment.id">
          <div class="card border-secondary border-bottom bg-dark text-white">
            <div class="card-body p-2">
              <p class="card-text mb-1 fw-bold">{{comment.username}}</p>
              <p class="card-text mb-0">{{comment.comment}}</p>
              <p class="card-text text-muted">{{comment.created_time}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.card {
  max-width: 60vw;
}
</style>
