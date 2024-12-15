<template>
    <div>
        <nav class="navbar bg-primary navbar-expand-lg" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/influencer/dashboard">SponserConnect | {{ profile.name
                    }}</router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end">
                    <div class="navbar-nav">
                        <router-link class="nav-link active" to="/influencer/profile">Profile</router-link>
                        <router-link class="nav-link active" to="/influencer/logout">Logout</router-link>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container mt-5">
            <h3 class="text-center">Profile</h3>
            <div class="row justify-content-center">
                <div class="col-md-6 bg-light p-3">
                    <form @submit.prevent="updateProfile">
                        <div class="mb-3">
                            <label for="email">Email</label>
                            <input type="email" class="form-control" id="email" v-model="profile.email" disabled />
                        </div>
                        <div class="mb-3">
                            <label for="name">Name</label>
                            <input type="text" class="form-control" id="name" v-model="profile.name" required />
                        </div>
                        <div class="mb-3">
                            <label for="niche">Niche</label>
                            <input type="text" class="form-control" id="niche" v-model="profile.niche" required />
                        </div>
                        <div class="mb-3">
                            <label for="reach">Reach (e.g. 100k, 1M etc.)</label>
                            <input type="text" class="form-control" id="reach" v-model="profile.reach" required />
                        </div>
                        <button type="submit" class="btn btn-primary mb-3">Save</button>
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
            profile: {
                email: "",
                name: "",
                niche: "",
                reach: ""
            },
        };
    },
    created() {
        this.fetchProfile();
    },
    methods: {
        async fetchProfile() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/influencer/profile", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${localStorage.getItem('influencerToken')}`
                    },
                });
                const data = await response.json();
                if (response.ok) {
                    this.profile = data;
                } else {
                    alert(data.msg)
                }
            } catch (error) {
                console.error("Error fetching profile:", error);
                alert("An error occurred while loading the profile.");
            }
        },
        async updateProfile() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/influencer/profile", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        'Authorization': `Bearer ${localStorage.getItem('influencerToken')}`
                    },
                    body: JSON.stringify(this.profile)
                });
                const data = await response.json()
                if (response.ok) {
                    alert(data.msg || "Profile updated successfully.");
                } else {
                    alert(data.msg || "Failed to update profile.");
                }
            } catch (error) {
                console.error("Error updating profile:", error);
                talert("An error occurred while updating the profile.");
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