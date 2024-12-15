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
            <h3 class="text-center">Create Ad Request</h3>

            <div class="row">
                <div class="col-md-8 bg-light p-3">
                    <form @submit.prevent="createAdRequest">
                        <div class="mb-3">
                            <label for="message">Message</label>
                            <textarea class="form-control" id="message" v-model="adRequest.message" rows="3"
                                required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="requirements">Requirements</label>
                            <textarea class="form-control" id="requirements" v-model="adRequest.requirements" rows="3"
                                required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="payment_amount">Payment Amount</label>
                            <input type="number" class="form-control" id="payment_amount"
                                v-model="adRequest.payment_amount" required />
                        </div>
                        <button type="submit" class="btn btn-primary mt-3 mb-3">Create Ad Request</button>
                    </form>
                </div>

                <div class="col-md-4 bg-light p-3">
                    <div class="mb-3">
                        <label for="search_influencer">Search Influencer</label>
                        <input type="text" class="form-control" id="search_influencer" v-model="searchQuery"
                            placeholder="Search by name" />
                    </div>
                    <div class="mt-3">
                        <div v-for="influencer in filteredInfluencers" :key="influencer.id"
                            class="card influencer-card mb-2">
                            <div class="card-body">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="influencer_id"
                                        :id="'influencer_' + influencer.id" :value="influencer.id"
                                        v-model="adRequest.influencer_id" required />
                                    <label class="form-check-label" :for="'influencer_' + influencer.id">
                                        {{ influencer.name }} [Niche: {{ influencer.niche }} | Reach: {{
                                        influencer.reach }}]
                                    </label>
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
            influencers: [],
            adRequest: {
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
                }); // Replace with actual API endpoint
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
        async createAdRequest() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/ad/create/${this.$route.params.ID}`, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                     },
                    body: JSON.stringify(this.adRequest),
                });
                const result = await response.json();

                if (response.ok) {
                    alert(result.msg || "Ad request created successfully!");
                    this.resetForm();
                    this.$router.push("/sponsor/dashboard");
                } else {
                    alert("Failed to create ad request. Please try again.");
                    this.$router.push("/sponsor/dashboard");
                }
            } catch (error) {
                alert("Error creating ad request.");
            }
        },
        resetForm() {
            this.adRequest = {
                message: "",
                requirements: "",
                payment_amount: null,
                influencer_id: null,
            };
        },
    },
    mounted(){
        this.fetchInfluencers();
    },
};
</script>

<style scoped>
body {
    background: #DEAC80;
}

.influencer-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>