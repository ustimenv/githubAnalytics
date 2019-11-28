
<template>
  <div id='bigDiv'>
      <div class="search">
        <div v-if="searching" class="container-search">
          <img src="/pendulum.gif" alt="Searching Icon">
        </div>

        <!--<form @submit.prevent="search">
          <input type="text" placeholder="Who are we searching?" v-model="searchee">
          <button id="submitButton" @click="search();">Search!</button>
        </form>-->

        <button id="submitButton" @click="search();">Search!</button>

        <h2 id='loggedIn'>
          Logged in as: {{username}}
        </h2>
        <div id='divovivo'>
        </div>
        <button id="nextButton" @click="nextGraph();">next</button>

      </div>
  </div>

</template>


<style scoped lang="scss">
  .bigDiv{
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
        h2 {
            position: fixed;
            top: 0px;
            right: 30px;
            width: 100px;
            height: 200px;
        }
        }
        divivo {
            position: fixed;
            heigh: 1000px;
    //        top: 0px;
    //        right: 30px;
    //        width: 100px;
    //        height: 200px;
        }
        nextButton {
            position: fixed;
            bottom: 40px;
        }
  }
</style>



<script>
const OctoRest = require("@octokit/rest");
const Plotly = require("plotly.js-dist");


  export default {
    beforeMount() {
//      this.octo = new OctoRest();
      this.octo = new OctoRest({
          auth: process.env.VUE_APP_TOKEN});
    },
    data: function() {
      return {
          result: null,
          complete: false,
          repoNames: [],
          result2: null,
          displayedRepoIndex: 0,
          displayedRepoName: ""
      }
    },
    props: {
        username: {
            type: String,
            default: 'Yeeehaw',
            },
//        octo1: {
//            type: Object,
//            default: new OctoRest(),
//            },
    },

    methods: {
      search() {
        //top level user overview
        this.octo.users.getByUsername({username:'ustimenv'})
        .then(resultA => {
          this.result = resultA.data
        })

        //Get repository names
        this.octo.repos.listForUser({
          username: 'ustimenv',
          type: 'owner'
        })
        .then(resultB => {
          for(var i = 0; i<resultB.data.length; i++)
          {
            this.repoNames.push(resultB.data[i].name)
          }
          var requests = [];

          for(var j=0; j<this.repoNames.length; j++)
          {
            requests.push(this.octo.repos.getContributorsStats({
              owner: 'ustimenv',
              repo: this.repoNames[j]
            }))
          }

          Promise.all(requests)
          .then(resultC => {

            this.complete = true
            var resultTmp = []

            for(var k=0; k<resultC.length; k++)
            {
              for(var m=0; m<resultC[k].data.length; m++)
              {
                if(resultC[k].data[m].author.login == 'ustimenv')
                {
                  resultTmp.push(resultC[k].data[m])
                }
              }
            }
            this.result2 = resultTmp
            this.visualiseRepo(0)
            })
        });
      },

      visualiseRepo(repoIndex) {
        var repo = this.result2[repoIndex]
        var additions = []
        var deletions = []
        var commits = []
        var weeks = []
        for(var i=0; i<repo.weeks.length; i++)
        {
          additions.push(repo.weeks[i].a)
          deletions.push(repo.weeks[i].d)
          weeks.push(new Date(repo.weeks[i].w * 1000))
          commits.push(repo.weeks[i].c)

        }
        //eslint-disable-next-line
//        console.log(repo)
        var A = {
            x: weeks,
            y: additions,
            name: 'Additions',
            type: 'bar'
        }
        var D = {
            x: weeks,
            y: deletions,
            name: 'Deletions',
            type: 'bar'
        }
        //eslint-disable-next-line
        var C = {
            x: weeks,
            y: commits,
            name: 'Commits',
            type: 'bar'
        }
//        var data = [A, D, C]
        var data = [A, D]
        var layout = {barmode: 'group'}
        Plotly.plot('divovivo', data, layout)
      },

    nextGraph() {
      var myDiv = document.getElementById('divovivo')
      myDiv.remove()
      var newMyDiv = document.createElement('div')
      newMyDiv.id = 'divovivo'
      document.getElementById('bigDiv').appendChild(newMyDiv)
      this.visualiseRepo(this.displayedRepoIndex)
      this.displayedRepoIndex++
    }

  }
}

</script>
