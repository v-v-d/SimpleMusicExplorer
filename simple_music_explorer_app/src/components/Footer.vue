<template>
  <div class="footer-copyright text-center py-3">© {{ new Date().getFullYear() }} Copyright:
    <router-link :to="{ name: 'Index' }" class="logo-link">Simple Music Explorer</router-link>
  </div>
</template>

<script>
  export default {
    name: "Footer",
  }
</script>

<style scoped>
  .footer-copyright {
    background-color: #333;
    box-sizing: border-box;
    padding-top: 1rem;
    padding-bottom: 1rem;
    text-align: center;
    overflow: hidden;
    color: rgba(255,255,255,0.6);
  }

  .logo-link:hover,
  .logo-link:active,
  .logo-link {
    color: unset;
    text-decoration: unset;
  }

</style>