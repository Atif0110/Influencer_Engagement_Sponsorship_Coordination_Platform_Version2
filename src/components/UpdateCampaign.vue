<template>
  <div>
    <nav class="navbar bg-primary navbar-expand-lg" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/sponsor/dashboard">SponsorConnect: Sponsor Dashboard</router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end">
                    <div class="navbar-nav">
                        <router-link class="nav-link active" to="/sponsor/campaign-create">Create Campaign</router-link>
                        <button class="nav-link active" @click="logout">Logout</button>
                    </div>
                </div>
            </div> 
        </nav>

    <div class="container mt-5">
      <h3 class="text-center">Update Campaign</h3>
      <div class="row mt-3 justify-content-center">
        <div class="col-lg-8 bg-light p-3">
          <form @submit.prevent="updateCampaign">
            <div class="row mb-3">
              <div class="col-md-8">
                <label for="name" class="form-label">Campaign Name</label>
                <input type="text" class="form-control" id="name" v-model="campaign.name" required />
              </div>
              <div class="col-md-4">
                <label for="budget" class="form-label">Budget</label>
                <input type="number" class="form-control" id="budget" v-model="campaign.budget" required />
              </div>
            </div>

            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea class="form-control" id="description" v-model="campaign.description" rows="3"
                required></textarea>
            </div>

            <div class="row mb-3">
              <div class="col-md-4">
                <label for="start_date" class="form-label">Start Date</label>
                <input type="date" class="form-control" id="start_date" v-model="campaign.start_date" required />
              </div>
              <div class="col-md-4">
                <label for="end_date" class="form-label">End Date</label>
                <input type="date" class="form-control" id="end_date" v-model="campaign.end_date" required />
              </div>
            </div>

            <button type="submit" class="btn btn-primary mb-3">Update Campaign</button>
          </form>
          <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaign: {
        name: "",
        budget: 0,
        description: "",
        start_date: "",
        end_date: ""
      },
      errorMessage: "" // to display error messages
    };
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Add leading zero if needed
      const day = String(date.getDate()).padStart(2, '0'); // Add leading zero if needed
      return `${year}-${month}-${day}`;
    },
    async updateCampaign() {
      console.log("Attempting to update campaign...");
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/campaign/update/${this.$route.params.ID}`, {
          method: "PUT", 
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("sponsorToken")}`
          },
          body: JSON.stringify(this.campaign)
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.msg || "Campaign updated successfully.");
          this.$router.push("/sponsor/dashboard");
        } else {
          this.errorMessage = result.msg || "Failed to update campaign.";
        }
      } catch (error) {
        console.error("Error updating campaign:", error);
        this.errorMessage = "An error occurred while updating the campaign.";
      }
    }
  },
  async mounted() {
    console.log("Fetching campaign details...");
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/campaign/${this.$route.params.ID}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("sponsorToken")}`
        }
      });

      if (response.ok) {
        const data = await response.json();

        // Format the dates to YYYY-MM-DD
        data.start_date = this.formatDate(data.start_date);
        data.end_date = this.formatDate(data.end_date);

        this.campaign = { ...data };
        console.log("Campaign details fetched successfully:", data);
      } else {
        this.errorMessage = "Failed to load campaign details.";
      }
    } catch (error) {
      console.error("Error fetching campaign details:", error);
      this.errorMessage = "An error occurred while loading campaign details.";
    }
  }
};
</script>

<style scoped>
body {
  background: #deac80;
}
</style>
