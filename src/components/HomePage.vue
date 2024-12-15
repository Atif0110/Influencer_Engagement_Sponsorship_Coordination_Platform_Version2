<template>
  <div class="container mt-5 text-center">
    <h1 class="display-4">Welcome to SponserConnect</h1>
    <p class="lead">Connecting Sponsors with Influencers for Effective Advertising</p>
    <hr class="my-4">

    <div class="row mt-5">
      <div class="col-md-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Sponsor Login</h5>
            <p class="card-text">Log in to manage your campaigns and connect with influencers.</p>
            <button @click="navigateTo('SponsorLogin')" class="btn btn-primary">Sponsor Login</button>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Influencer Login</h5>
            <p class="card-text">Log in to find campaigns and connect with sponsors.</p>
            <button @click="navigateTo('InfluencerLogin')" class="btn btn-primary">Influencer Login</button>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Admin Login</h5>
            <p class="card-text">Log in to monitor users, campaigns, and statistics.</p>
            <button @click="navigateTo('AdminLogin')" class="btn btn-primary">Admin Login</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    navigateTo(routeName) {
      this.$router.push({ name: routeName });
    },
  },
};
</script>

<style scoped>

</style>
