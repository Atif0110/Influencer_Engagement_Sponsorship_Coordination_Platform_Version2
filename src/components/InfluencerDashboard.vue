<template>
    <div>
        <nav class="navbar bg-primary navbar-expand-lg" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/influencer/dashboard">SponsorConnect: Influencer
                    Dashboard</router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end">
                    <div class="navbar-nav">
                        <router-link class="nav-link active" to="/influencer/profile">Profile</router-link>
                        <button class="nav-link active" @click="logout">Logout</button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container mt-5">
            <div class="mb-3">
                <input type="text" class="form-control" placeholder="Search by industry" v-model="searchQuery" />
            </div>

            <div class="row">
                <div v-for="campaign in filteredCampaigns" :key="campaign.id" class="col-md-4 mb-4 campaign-card">
                    <div class="card h-100 cam-card">
                        <div class="card-body">
                            <h5 class="card-title">
                                {{ campaign.name }}
                                <span class="badge text-bg-warning ind-text">{{ campaign.industry }}</span>
                            </h5>
                            <p class="card-description">{{ campaign.description.slice(0, 100) }}<span
                                    v-if="campaign.description.length > 100">...</span></p>
                            <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
                            <p class="card-text">
                                <strong>Visibility:</strong> {{ campaign.visibility }}
                                <span class="badge text-bg-danger" v-if="campaign.flagged">Flagged</span>
                            </p>
                            <button @click="requestCampaign(campaign.id)" class="btn btn-info">Request</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container mt-5">
            <div class="row">
                <div v-for="request in requests.reverse()" :key="request.id" class="col-md-12 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">
                                {{ request.campaign_name }}
                                <span class="badge text-bg-danger" v-if="request.flagged">Flagged</span>
                            </h5>
                            <p class="card-description"><strong>Description:</strong> {{ request.campaign_description }}
                            </p>
                            <p class="card-description"><strong>Requirements:</strong> {{ request.requirements }}</p>
                            <p class="card-description"><strong>Message:</strong> {{ request.message }}</p>
                            <p class="card-description">
                                <strong>Negotiation Terms:</strong>
                                <span v-if="!request.negotiation" class="badge text-bg-warning">Not Negotiated</span>
                                <span v-else>&nbsp; {{ request.negotiation }}</span>
                            </p>
                            <p class="card-text">
                                <strong>Payment:</strong> ${{ request.payment_amount }}
                                <span style="margin-left: 50px;"><strong>Status:</strong> {{ request.status }}</span>
                            </p>
                            <div v-if="request.message != 'This is a public campaign.'">
                            <button @click="updateRequestStatus(request.id, 'accept')" class="btn btn-success"
                                :disabled="request.status === 'Accepted' || request.status === 'Completed'">Accept</button>
                            <button @click="updateRequestStatus(request.id, 'reject')" class="btn btn-danger"
                                :disabled="['Accepted', 'Rejected', 'Completed'].includes(request.status)">Reject</button>
                            <button @click="submitNegotiation(request.id)" class="btn btn-info"
                                :disabled="request.status === 'Accepted' || request.status === 'Completed'">Negotiate</button>
                            <button @click="updateRequestStatus(request.id, 'complete')" class="btn btn-info"
                                :disabled="request.status !== 'Accepted' || request.status === 'Completed'">Completed</button>
                            </div>
                            <div v-else>
                            <button @click="updateRequestStatus(request.id, 'complete')" class="btn btn-info"
                                :disabled="request.status !== 'Accepted(Self)' || request.status === 'Completed'">Completed</button>
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
            searchQuery: "",
            campaigns: [],
            filteredCampaigns: [],
            requests: []
        };
    },
    computed: {
        filteredCampaigns() {
            return this.campaigns.filter((campaign) =>
                campaign.name.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    methods: {
        async fetchData() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/influencer/dashboard', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('influencerToken')}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    this.requests = data.requests;
                    this.campaigns = data.campaigns;
                } else {
                    alert("Failed to load campaigns.");
                }
            } catch (error) {
                alert("Error fetching campaigns:", error);
            }
        },
        async requestCampaign(campaignId) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/adrequest/create/${campaignId}`, {
                    method: "POST",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('influencerToken')}`
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.msg);
                    this.fetchData();
                } else {
                    alert(data.msg);
                }
            } catch (error) {
                alert("An error occurred while requesting the campaign.");
            }
        },
        logout() {
            localStorage.removeItem('influencerToken')
            this.$router.push('/influencer/login')
        },
        async updateRequestStatus(requestId, status) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/adrequest/${status}/${requestId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${localStorage.getItem('influencerToken')}`
                    },
                });

                const data = await response.json();
                if (response.ok) {
                    alert(data.msg)
                    this.fetchData();
                }
            } catch (error) {
                console.error("Error updating request status:", error);
            }
        },
        async submitNegotiation(requestId) {
            try {
                const negotiationMessage = prompt("Enter your negotiation message:");

                if (!negotiationMessage) {
                    alert("Negotiation message cannot be empty.");
                    return;
                }
                const response = await fetch(`http://127.0.0.1:5000/api/adrequest/negotiate/${requestId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${localStorage.getItem('influencerToken')}`
                    },
                    body: JSON.stringify({ message: negotiationMessage })
                });

                const data = await response.json();
                if (response.ok) {
                    alert(data.msg);
                    this.fetchData(); 
                } else {
                    alert(data.msg || "Failed to submit negotiation.");
                }
            } catch (error) {
                console.error("Error submitting negotiation:", error);
                alert("An error occurred while submitting the negotiation.");
            }
        }


    },
    created() {
        this.fetchData();
    }
};
</script>

<style scoped>
body {
    background: #deac80;
}
</style>