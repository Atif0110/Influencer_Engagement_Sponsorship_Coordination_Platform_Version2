<template>
    <div class="container mt-5">
        <h3 class="text-center">Sponsor Login</h3>

        <div class="row justify-content-center mt-3">
            <div class="col-md-4 bg-light p-3">
                <form @submit.prevent="handleLogin">
                    <div class="form-group">
                        <label for="company_name">Company Name</label>
                        <input type="text" class="form-control" id="company_name" v-model="company_name" required />
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" v-model="password" required />
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">Login</button>
                    <hr />
                    <div>Don't have an account? <router-link to="/sponsor/register">Register</router-link></div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            company_name: "",
            password: "",
        };
    },
    methods: {
        async handleLogin() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/sponsor/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        company_name: this.company_name,
                        password: this.password
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    localStorage.setItem('sponsorToken', data.token)
                    alert(data.msg)
                    this.$router.push("/sponsor/dashboard");
                } else {
                    alert(data.msg)
                }
            } catch (error) {
                alert("Login error:", error);
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