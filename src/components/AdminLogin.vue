<template>
    <div class="container mt-5">
        <h3 class="text-center">Admin Login</h3>

        <div v-if="message" class="row mt-3 justify-content-center">
            <span class="badge bg-info text-white">{{ message }}</span>
        </div>

        <div class="row justify-content-center mt-3">
            <div class="col-md-4 bg-light p-3">
                <form @submit.prevent="loginAdmin">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" class="form-control" id="username" value="Admin" disabled />
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" v-model="password" required />
                    </div>
                    <button type="submit" class="btn btn-primary mt-2">Login</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            password: '',
            message: '',
        };
    },
    methods: {
        async loginAdmin() {
            try {
                const response = await fetch("http://localhost:5000/api/admin/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        username: "Admin",
                        password: this.password,
                    }),
                });
                const data = await response.json();

                if (response.ok) {
                    this.message = "Login successful!";
                    localStorage.setItem("adminToken", data.token); 
                    this.$router.push({ name: "AdminDashboard" }); 
                } else {
                    this.message = data.message || "Login failed!";
                }
            } catch (error) {
                this.message = "An error occurred!";
            }
        },
    },
};
</script>

