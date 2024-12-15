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
                <div class="col-md-12 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Campaign: {{ campaign.name }}</h5>
                            <p class="card-description">{{ campaign.description }}</p>
                            <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
                            <p class="card-text">
                                <strong>Visibility:</strong> {{ campaign.visibility }}
                                <span v-if="campaign.flagged" class="badge text-bg-danger">Flagged</span>
                            </p>
                            <router-link :to="`/sponsor/campaign-update/${campaign.id}`"
                                class="btn btn-warning">Update</router-link>
                            <button @click="deleteCampaign(campaign.id)" class="btn btn-danger">Delete</button>
                            <router-link :to="`/sponsor/campaign-request/${campaign.id}`" class="btn btn-info">Request
                                Ad</router-link>
                        </div>
                    </div>
                </div>

                <div v-for="request in requests" :key="request.id" class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Influencer: {{ request.influencer }}</h5>
                            <p class="card-description"><strong>Requirements:</strong> {{ request.requirements }}</p>
                            <p class="card-text"><strong>Payment Amount:</strong> ${{ request.payment_amount }}</p>
                            <p class="card-text"><strong>Status:</strong> {{ request.status }}</p>
                            <p class="card-description">
                                <strong>Negotiation Terms:</strong>
                                <span v-if="!request.negotiation" class="badge text-bg-warning">Not Negotiated</span>
                                <span v-else>&nbsp; {{ request.negotiation }}</span>
                            </p>
                            <p class="card-description"><strong>Message:</strong> {{ request.message }}</p>

                            <div>
                                <button
                                    v-if="request.status !== 'Self Requested' && request.status !== 'Rejected(Self)' && request.status !== 'Accepted(Self)' && request.status !== 'Completed'"
                                    :class="{ 'btn btn-warning': true, disabled: request.status === 'Accepted' || request.status === 'Completed' }"
                                    @click="updateRequest(request.id)">
                                    Update
                                </button>
                                <button
                                    v-if="request.status !== 'Self Requested' && request.status !== 'Rejected(Self)' && request.status !== 'Accepted(Self)' && request.status !== 'Completed'"
                                    :class="{ 'btn btn-danger': true, disabled: request.status === 'Accepted' }"
                                    @click="deleteRequest(request.id)">
                                    Delete
                                </button>

                                <div v-else-if="request.status !== 'Completed'">
                                    <button
                                        :class="{ 'btn btn-danger': true, disabled: request.status === 'Accepted(Self)' }"
                                        @click="handleSelfRequest(request.id, 'DELETE')">
                                        Delete
                                    </button>
                                    <button
                                        :class="{ 'btn btn-success': true, disabled: request.status === 'Accepted(Self)' }"
                                        @click="handleSelfRequest(request.id, 'PATCH')">
                                        Accept
                                    </button>
                                    <button
                                        :class="{ 'btn btn-secondary': true, disabled: request.status === 'Accepted(Self)' }"
                                        @click="handleSelfRequest(request.id, 'PUT')">
                                        Reject
                                    </button>
                                </div>
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
            campaign: {
                name: "Campaign Name",
                description: "Campaign Description",
                budget: 5000,
                visibility: "Public",
                flagged: false,
                id: 1
            },
            requests: []
        };
    },
    created() {
        this.fetchCampaignsAndRequests();
    },
    methods: {
        async fetchCampaignsAndRequests() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/sponsor/campaign/${this.$route.params.ID}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    }
                }); // Replace with actual API endpoint
                const data = await response.json();
                if (response.ok) {
                    this.campaign = data.campaign;
                    this.requests = data.requests;
                } else {
                    alert("Failed to load campaigns.");
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
                    this.$router.push('/sponsor/dashboard')
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
        async deleteRequest(adId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/sponsor/ad/${adId}`, {
                    method: "DELETE",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    },
                });
                if (response.ok) {
                    this.fetchCampaignsAndRequests();
                    alert("Ad deleted successfully.");
                } else {
                    alert("Failed to delete Ad.");
                }
            } catch (error) {
                alert("An error occurred while deleting the Ad.");
            }
        },
        async updateRequest(id) {
            this.$router.push(`/sponsor/request-update/${id}`);
        },
        async handleSelfRequest(id, meth) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/campaign/request/${id}`, {
                    method: meth,
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.msg);
                    this.fetchCampaignsAndRequests();
                } else {
                    alert(data.msg);
                }
            } catch (error) {
                console.log("Error accepting request:", error);
            }
        },

    }
};
</script>

<style scoped>
body {
    background: #deac80;
}
</style>