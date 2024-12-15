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
            <h3 class="text-center">Update Ad Request</h3>

            <div class="row justify-content-center">
                <div class="col-md-8 bg-light p-3">
                    <form @submit.prevent="updateAdRequest">
                        <div class="mb-2">
                            <label for="campaign_id">Campaign</label>
                            <input type="text" class="form-control" id="campaign_id" :value="adRequest.campaign"
                                disabled />
                        </div>
                        <div class="mb-2">
                            <label for="influencer">Influencer</label>
                            <input type="text" class="form-control" id="influencer" :value="adRequest.influencer"
                                disabled />
                        </div>
                        <div class="mb-2">
                            <label for="message">Message</label>
                            <textarea class="form-control" id="message" v-model="adRequest.message" rows="3"
                                required></textarea>
                        </div>
                        <div class="mb-2">
                            <label for="requirements">Requirements</label>
                            <textarea class="form-control" id="requirements" v-model="adRequest.requirements" rows="3"
                                required></textarea>
                        </div>
                        <div class="mb-2">
                            <label for="payment_amount">Payment Amount</label>
                            <input type="number" class="form-control" id="payment_amount" v-model="adRequest.payment_amount"
                                required />
                        </div>
                        <button type="submit" class="btn btn-primary mt-3">Update Ad Request</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            influencers: [],
            adRequest: {
                campaign: "",
                influencer: "",
                message: "",
                requirements: "",
                payment_amount: null,
                influencer_id: null,
            },
            searchQuery: "",
        };
    },
    computed: {
        filteredInfluencers() {
            return this.influencers.filter((influencer) =>
                influencer.name.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    methods: {
        async fetchInfluencers() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/influencers', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    }
                }); 
                const data = await response.json();
                if (response.ok) {
                    this.influencers = data;
                    console.log(data)
                } else {
                    alert("Failed to load influencers.");
                }
            } catch (error) {
                alert("Error fetching influencers:", error);
            }
        },
        async fetchAd() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/sponsor/ad/${this.$route.params.ID}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                    }
                }); 
                const data = await response.json();
                if (response.ok) {
                    this.adRequest = {...data.ad}
                } else {
                    alert("Failed to load influencers.");
                }
            } catch (error) {
                alert("Error fetching influencers:", error);
            }
        },
        async updateAdRequest() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/sponsor/ad/${this.$route.params.ID}`, {
                    method: "PUT",
                    headers: { 
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                     },
                    body: JSON.stringify(this.adRequest),
                });
                const result = await response.json();

                if (response.ok) {
                    alert(result.msg || "Ad request updated successfully!");
                    this.$router.push("/sponsor/dashboard");
                } else {
                    alert("Failed to create ad request. Please try again.");
                    this.$router.push("/sponsor/dashboard");
                }
            } catch (error) {
                alert("Error updating ad request.");
            }
        },
    },
    mounted(){
        this.fetchInfluencers();
        this.fetchAd();
    },
};
</script>

<style scoped>
body {
    background: #deac80;
}
</style>