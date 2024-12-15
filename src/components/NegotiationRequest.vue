<template>
    <div>
        <nav class="navbar bg-primary navbar-expand-lg" data-bs-theme="dark">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/influencer/dashboard">SponserConnect | {{ influencer
                    }}</router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse justify-content-end">
                    <div class="navbar-nav">
                        <router-link class="nav-link active" to="/influencer/logout">Logout</router-link>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container mt-5">
            <div class="row">
                <div v-if="messages.length" class="row justify-content-center">
                    <div v-for="(message, index) in messages" :key="index"
                        class="alert alert-info alert-dismissible fade show p-2 mt-1 col-md-8" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close p-2" @click="closeMessage(index)"
                            aria-label="Close"></button>
                    </div>
                </div>
            </div>

            <div class="row justify-content-center">
                <div class="col-md-8 bg-light">
                    <form @submit.prevent="submitNegotiation">
                        <div class="mb-2">
                            <label for="campaign_id">Campaign</label>
                            <input type="text" class="form-control" id="campaign_id" :value="request.campaign.name"
                                disabled />
                        </div>
                        <div class="mb-2">
                            <label for="message">Message</label>
                            <textarea class="form-control" id="message" :value="request.message" rows="3"
                                disabled></textarea>
                        </div>
                        <div class="mb-2">
                            <label for="requirements">Requirements</label>
                            <textarea class="form-control" id="requirements" :value="request.requirements" rows="3"
                                disabled></textarea>
                        </div>
                        <div class="mb-2">
                            <label for="payment_amount">Payment Amount</label>
                            <input type="number" class="form-control" id="payment_amount"
                                :value="request.payment_amount" disabled />
                        </div>
                        <div class="mb-2">
                            <label for="negotiation_terms">Negotiation Terms</label>
                            <textarea class="form-control" id="negotiation_terms" v-model="form.negotiation" rows="3"
                                required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary mt-3 mb-3">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        influencer: {
            type: String,
            default: "Influencer Name"
        },
        request: {
            type: Object,
            required: true,
            default: () => ({
                campaign: { name: "" },
                message: "",
                requirements: "",
                payment_amount: 0,
                negotiation: ""
            })
        }
    },
    data() {
        return {
            form: {
                negotiation: this.request.negotiation || ""
            },
            messages: []
        };
    },
    methods: {
        async submitNegotiation() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/request/negotiate/${this.request.id}`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ negotiation: this.form.negotiation })
                });

                if (response.ok) {
                    this.messages.push("Negotiation submitted successfully.");
                    this.form.negotiation = ""; // Clear the form
                } else {
                    const errorData = await response.json();
                    this.messages.push(errorData.message || "Failed to submit negotiation.");
                }
            } catch (error) {
                console.error("Error:", error);
                this.messages.push("An error occurred. Please try again later.");
            }
        },
        closeMessage(index) {
            this.messages.splice(index, 1);
        }
    }
};
</script>

<style scoped>
body {
    background: #deac80;
}
</style>