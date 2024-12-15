<template>
    <div class="container mt-5">
        <h3 class="text-center">Influencer Login</h3>
        <!-- Login Form -->
        <div class="row mt-3 justify-content-center">
            <div class="col-md-4 bg-light p-3">
                <form @submit.prevent="handleLogin">
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" v-model="email" required />
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" v-model="password" required />
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">Login</button>
                    <hr />
                    <div>Don't have an account? <router-link to="/influencer/register">Register</router-link></div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: "",
            password: "",
        };
    },
    methods: {
        async handleLogin() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/influencer/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    })
                });

                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('influencerToken', data.token)
                    this.$router.push("/influencer/dashboard");
                    alert(data.msg)
                } else {
                    alert(data.msg);
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("An error occurred. Please try again later.");
            }
        }
    }
};
</script>

<style scoped>
body {
    background: #deac80;
}
</style>