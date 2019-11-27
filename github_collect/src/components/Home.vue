<template>
  <div class="home">
    <h1>{{ msg }}</h1>
  </div>
</template>


<template>
  <div class="search">
    <div v-if="searching" class="container-search">
      <img src="/pendulum.gif" alt="Searching Icon">
    </div>

    <form @submit.prevent="searchSubmit">
      <input type="text" placeholder="Who are we searching?" v-model="name">

      <button id="submitButton" @click="search();">Search</button>


    </form>
  </div>
</template>


<style scoped lang="scss">
  .search {
    border: 1px solid black;
    border-radius: 5px;
    padding: 1.5rem;
    width: 300px;
    margin-left: auto;
    margin-right: auto;
    position: relative;
    overflow: hidden;
    .container-loading {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: rgba(0,0,0,.3);
      img {
        width: 2rem;
        height: 2rem;
      }
    }
    form {
      display: flex;
      flex-flow: column;
      *:not(:last-child) {
        margin-bottom: 1rem;
      }
      input {
        padding: .5rem;
      }
      button {
        padding: .5rem;
        background-color: lightgray;
        border: 1px solid gray;
        border-radius: 3px;
        cursor: pointer;
        &:hover {
          background-color: lightslategray;
        }
      }
    }
  }
</style>


<script>
  export default {
    methods: {
      initialise() {
        const Octokit = require("@octokit/rest");

        this.$octo =  new Octokit({
          auth: {
//            username: "octocat",
//            password: "secret",
            async on2fa() {
//               example: ask the user
              return prompt("Two-factor authentication Code:");
            }
          }
        });

      },

      search() {
        this.$octo.repos
        .listForOrg({
            org: "octokit",
            type: "public"
        })
        .then(({ data, headers, status }) => {
            alert("EEE")
            alert(data)
            // eslint-disable-next-line no-console
            console.log(headers)
            // eslint-disable-next-line no-console
            console.log(status)

        });
      }


    },
    beforeMount() {
      this.initialise()
    }
  }
</script>
