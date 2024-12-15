<template>
    <div>
        <nav class="navbar bg-primary navbar-expand-lg" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/sponsor/dashboard">SponsorConnect: Sponsor
                    Dashboard</router-link>
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

            <div class="row">
                <div v-for="campaign in campaigns" :key="campaign.id" class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <router-link :to="`/sponsor/campaign/${campaign.id}`"
                                class="text-decoration-none text-black">
                                <h5 class="card-title">{{ campaign.name }}</h5>
                                <p class="card-description">{{ campaign.description }}</p>
                                <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
                                <p class="card-text"><strong>Visibility:</strong> {{ campaign.visibility }}
                                    <span v-if="campaign.flagged" class="badge text-bg-danger">Flagged</span>
                                </p>
                            </router-link>
                            <div class="mt-3">
                                <router-link :to="`/sponsor/campaign-update/${campaign.id}`"
                                    class="btn btn-warning">Update</router-link>
                                <button @click="deleteCampaign(campaign.id)" class="btn btn-danger">Delete</button>
                                <router-link :to="`/sponsor/campaign-request/${campaign.id}`"
                                    class="btn btn-info">Request
                                    Ad</router-link>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            campaigns: [], 
        };
    },
    created() {
        this.fetchCampaigns();
    },
    methods: {
        async fetchCampaigns() {
            // console.log(localStorage.getItem('sponsorToken'))
            try {
                const response = await fetch('http://127.0.0.1:5000/api/sponsor/dashboard', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    }
                }); // Replace with actual API endpoint
                const data = await response.json();
                if (response.ok) {
                    this.campaigns = data;
                } else {
                    alert(data.msg || "Failed to load campaigns.");
                }
            } catch (error) {
                alert("Error fetching campaigns:", error);
            }
        },
        async deleteCampaign(campaignId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/campaign/delete/${campaignId}`, {
                    method: "DELETE",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    },
                });
                if (response.ok) {
                    this.fetchCampaigns();
                    alert("Campaign deleted successfully.");
                } else {
                    alert("Failed to delete campaign.");
                }
            } catch (error) {
                alert("An error occurred while deleting the campaign.");
            }
        },
        logout() {
            localStorage.removeItem('sponsorToken')
            this.$router.push('/sponsor/login')
        },
    }
};
</script>

<style scoped>
body {
    background: #deac80;
}

.card-description {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    /* Show only 2 lines */
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 3em;
    /* Approximate height for 2 lines of text */
}
</style>