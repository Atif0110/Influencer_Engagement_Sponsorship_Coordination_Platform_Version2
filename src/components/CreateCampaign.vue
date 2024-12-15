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
            <h3 class="text-center">Create Campaign</h3>
            <div class="row mt-2 justify-content-center">
                <div class="col-lg-8 bg-light p-3">

                    <form @submit.prevent="createCampaign">
                        <div class="row mb-3">
                            <div class="col-md-8">
                                <label for="name" class="form-label">Campaign Name</label>
                                <input type="text" class="form-control" id="name" v-model="campaign.name" required />
                            </div>
                            <div class="col-md-4">
                                <label for="budget" class="form-label">Budget</label>
                                <input type="number" class="form-control" id="budget" v-model="campaign.budget"
                                    required />
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
                                <input type="date" class="form-control" id="start_date" v-model="campaign.start_date"
                                    required />
                            </div>
                            <div class="col-md-4">
                                <label for="end_date" class="form-label">End Date</label>
                                <input type="date" class="form-control" id="end_date" v-model="campaign.end_date"
                                    required />
                            </div>
                            <div class="col-md-4">
                                <label for="visibility" class="form-label">Visibility</label>
                                <select class="form-select" id="visibility" v-model="campaign.visibility" required>
                                    <option value="Private">Private</option>
                                    <option value="Public">Public</option>
                                </select>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary mb-3">Create Campaign</button>
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
            campaign: {
                name: "",
                budget: null,
                description: "",
                start_date: "",
                end_date: "",
                visibility: "Private",
            },
        };
    },
    methods: {
        async createCampaign() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/campaign/create', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('sponsorToken')}`
                     },
                    body: JSON.stringify(this.campaign),
                });
                const result = await response.json();

                if (response.ok) {
                    alert(result.msg);
                    this.clearForm();
                    this.$router.push("/sponsor/dashboard");
                } else {
                    alert(result.msg);
                    this.$router.push("/sponsor/dashboard");
                }
            } catch (error) {
                alert("Error creating campaign.");
            }
        },
        clearForm() {
            this.campaign = {
                name: "",
                budget: null,
                description: "",
                start_date: "",
                end_date: "",
                visibility: "Private",
            };
        },
    },
};
</script>
