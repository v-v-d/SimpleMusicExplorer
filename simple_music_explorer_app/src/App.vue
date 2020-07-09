<template>
  <div id="app">
    <div class="wrapper">
      <div class="top">
        <NavBar/>
        <router-view/>
      </div>

      <Footer/>
    </div>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  import Footer from '@/components/Footer.vue'
  import { mapGetters, mapActions } from "vuex";

  export default {
    name: 'App',
    components: {
      NavBar,
      Footer,
    },
    computed: mapGetters(['isToken']),
    methods: mapActions(['getTokenFromLocalStorage', 'getUser']),
    mounted() {
      this.getTokenFromLocalStorage();

      if (this.isToken) {
        this.getUser();
      }
    }
  }
</script>

<style>
  * {
    margin: 0;
    padding: 0;
  }

  html,
  body {
    height: 100%;
  }

  .wrapper {
    min-height: 100%;
    display: flex;
    flex-direction: column;
  }

  .top {
    flex-grow: 1;
  }

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }
</style>

<!--<template>-->
<!--  <div id="app">-->
<!--    <div id="nav">-->
<!--      <router-link to="/">Home</router-link> |-->
<!--      <router-link to="/about">About</router-link>-->
<!--    </div>-->
<!--    <router-view/>-->
<!--  </div>-->
<!--</template>-->

<!--<style>-->
<!--#app {-->
<!--  font-family: Avenir, Helvetica, Arial, sans-serif;-->
<!--  -webkit-font-smoothing: antialiased;-->
<!--  -moz-osx-font-smoothing: grayscale;-->
<!--  text-align: center;-->
<!--  color: #2c3e50;-->
<!--}-->

<!--#nav {-->
<!--  padding: 30px;-->
<!--}-->

<!--#nav a {-->
<!--  font-weight: bold;-->
<!--  color: #2c3e50;-->
<!--}-->

<!--#nav a.router-link-exact-active {-->
<!--  color: #42b983;-->
<!--}-->
<!--</style>-->
