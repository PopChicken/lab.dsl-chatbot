<template>
  <router-view />
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import Portal from '@/views/Portal.vue';

@Options({
  components: {
    Portal
  },
})
export default class App extends Vue {}
</script>

<style>
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

@media screen and (min-width: 961px) {
  body {
    padding-top: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgb(92, 34, 35);
    background-image: url("~@/assets/images/texture.png");
  }
}

@media screen and (max-width: 960px) {
  body {
    display: flex;
    margin: 0;
    width: 100vw;
    height: 100vh;
    background-color: white;
    background-image: url("~@/assets/images/texture.png");
  }
}

</style>
