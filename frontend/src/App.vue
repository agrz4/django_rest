<template>
  <div id="app">
    <h1>School Management Dashboard</h1>
    <Dashboard />
  </div>
</template>

<script>
import Dashboard from './components/Dashboard.vue';

export default {
  name: 'App',
  components: {
    Dashboard
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}
h1 {
  color: #34495e;
  border-bottom: 2px solid #42b983;
  padding-bottom: 10px;
  display: inline-block;
}
</style>