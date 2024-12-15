<template>
    <div class="container mt-5">
        <h3 class="text-center">Influencer Registration</h3>

        <div class="row mt-3 justify-content-center">
            <div class="col-md-4 bg-light p-3">
                <form @submit.prevent="register">
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" class="form-control" id="name" v-model="form.name" required />
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" v-model="form.email" required />
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" v-model="form.password" required />
                    </div>
                    <div class="form-group">
                        <label for="niche">Niche</label>
                        <input type="text" class="form-control" id="niche" v-model="form.niche" required />
                    </div>
                    <div class="form-group">
                        <label for="reach">Reach (e.g. 100k, 1M etc.)</label>
                        <input type="text" class="form-control" id="reach" v-model="form.reach" required />
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">Register</button>
                    <hr />
                    <div>Already have an account? <router-link to="/influencer/login">Login</router-link></div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            form: {
                name: "",
                email: "",
                password: "",
                niche: "",
                reach: ""
            },
            messages: []
        };
    },
    methods: {
        async register() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/influencer/register", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(this.form)
                });

                const data = await response.json();
                if (response.ok) {
                    alert(data.msg || "Registration successful! Please login.");
                    this.clearForm();
                    this.$router.push("/influencer/login");
                } else {
                    alert(data.message || "Registration failed. Please try again.");
                }
            } catch (error) {
                alert("An error occurred. Please try again later.");
            }
        },
        clearForm() {
            this.form = {
                name: "",
                email: "",
                password: "",
                niche: "",
                reach: ""
            };
        }
    }
};
</script>

<style scoped>
body {
    background: #deac80;
}
</style>