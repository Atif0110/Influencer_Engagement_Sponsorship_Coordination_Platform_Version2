<template>
    <div>
        <nav class="navbar bg-primary navbar-expand-lg" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" href="/admin/dashboard">SponserConnect: Admin</router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end">
                    <div class="navbar-nav">
                        <button class="nav-link active" @click="logout">Logout</button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container mt-5">

            <div class="row mt-3">
                <div class="card p-3 mt-2 col-md-3 bg-primary fw-bold text-white">Total Sponsors <span>{{
                    total_sponsors }}</span></div>
                <div class="card p-3 mt-2 col-md-3 bg-success fw-bold text-white">Total Influencers <span>{{
                    total_influencers }}</span></div>
                <div class="card p-3 mt-2 col-md-3 bg-danger fw-bold text-white">Total Campaigns <span>{{
                    campaigns.length }}</span></div>
                <div class="card p-3 mt-2 col-md-3 bg-secondary fw-bold text-white">Total Ad Requests <span>{{
                    total_ads }}</span></div>
            </div>
        </div>

        <div class="container mt-5">
            <div class="row">
                <div class="col-md-12 mb-4" v-for="campaign in campaigns" :key="campaign.id">
                    <div class="card h-80">
                        <div class="card-body">
                            <h5 class="card-title">{{ campaign.name }}</h5>
                            <p class="card-description">{{ campaign.description }}</p>
                            <p class="card-text">
                                <strong>Visibility:</strong> {{ campaign.visibility }} &nbsp;&nbsp;&nbsp;&nbsp;
                                <span v-if="campaign.flagged" class="badge text-bg-danger">Flagged</span>
                            </p>
                            <button @click="toggleFlag(campaign.id)"
                                :class="campaign.flagged ? 'btn btn-success' : 'btn btn-danger'">
                                {{ campaign.flagged ? 'Remove Flag' : 'Flag' }}
                            </button>
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
            total_sponsors: 0,
            total_influencers: 0,
            total_ads: 0,
            campaigns: [],
        };
    },
    created() {
        this.fetchData();
    },
    methods: {
        async fetchData() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/admin/dashboard', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    this.total_sponsors = data.total_sponsors;
                    this.total_influencers = data.total_influencers;
                    this.total_ads = data.total_ads;
                    this.campaigns = data.campaigns;
                } else {
                    alert("Failed to load data.");
                }
            } catch (error) {
                alert("Error fetching data:", error);
            }
        },
        logout() {
            localStorage.removeItem('adminToken')
            this.$router.push('/admin/login')
        },
        async toggleFlag(campaignId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/campaign/${campaignId}/flag`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
                    },
                });
                const result = await response.json();

                if (response.ok) {
                    alert(result.msg)
                    this.fetchData();
                }
            } catch (error) {
                this.messages.push('Error updating campaign status');
            }
        },
    },
};
</script>

<style scoped>
body {
    background: #DEAC80;
}
</style>