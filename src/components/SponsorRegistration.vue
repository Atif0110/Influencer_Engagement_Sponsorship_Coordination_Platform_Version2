<template>
    <div class="container mt-5">
        <h3 class="text-center">Sponsor Registration</h3>

        <div class="row justify-content-center mt-3">
            <div class="col-md-4 bg-light p-3">
                <form @submit.prevent="handleRegister">
                    <div class="form-group">
                        <label for="company_name">Company Name</label>
                        <input type="text" class="form-control" id="company_name" v-model="company_name" required />
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" class="form-control" id="email" v-model="email" required />
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" v-model="password" required />
                    </div>
                    <div class="form-group">
                        <label for="industry">Industry</label>
                        <input type="text" class="form-control" id="industry" v-model="industry" required />
                    </div>
                    <button type="submit" class="btn btn-primary mt-3">Register</button>
                    <hr />
                    <div>Already have an account? <router-link to="/sponsor/login">Login</router-link></div>
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
            email: "",
            industry: "",
        };
    },
    methods: {
        async handleRegister() {
            try {
                const response = await fetch("http://127.0.0.1:5000/api/sponsor/register", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        company_name: this.company_name,
                        password: this.password,
                        email: this.email,
                        industry: this.industry
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.msg)
                    this.$router.push("/sponsor/login");
                } else {
                    alert(data.msg)
                }
            } catch (error) {
                alert("Registration error:", error);
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