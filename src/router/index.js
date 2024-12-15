import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../components/HomePage.vue';
import AdminLogin from '../components/AdminLogin.vue';
import InfluencerLogin from '../components/InfluencerLogin.vue';
import SponsorLogin from '../components/SponsorLogin.vue';
import InfluencerRegistration from '../components/InfluencerRegistration.vue';
import SponsorRegistration from '../components/SponsorRegistration.vue';

import AdminDashboard from '../components/AdminDashboard.vue';
import SponsorDashboard from '../components/SponsorDashboard.vue';
import CreateCampaign from '../components/CreateCampaign.vue';
import UpdateCampaign from '../components/UpdateCampaign.vue';

import InfluencerDashboard from '../components/InfluencerDashboard.vue';
import InfluencerProfile from '../components/InfluencerProfile.vue';
import CreateAdRequest from '../components/CreateAdRequest.vue';
import UpdateRequest from '../components/UpdateRequest.vue';
import SponsorCampaigns from '../components/SponsorCampaigns.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/admin/login', name: 'AdminLogin', component: AdminLogin },
  { path: '/influencer/login', name: 'InfluencerLogin', component: InfluencerLogin },
  { path: '/sponsor/login', name: 'SponsorLogin', component: SponsorLogin },
  { path: '/influencer/register', name: 'InfluencerRegistration', component: InfluencerRegistration },
  { path: '/sponsor/register', name: 'SponsorRegistration', component: SponsorRegistration },

  { path: '/sponsor/dashboard', name: 'SponsorDashboard', component: SponsorDashboard },
  { path: '/sponsor/campaign/:ID', name: 'SponsorCampaigns', component: SponsorCampaigns },
  { path: '/sponsor/campaign-create', name: 'CreateCampaign', component: CreateCampaign },
  { path: '/sponsor/campaign-update/:ID', name: 'UpdateCampaign', component: UpdateCampaign },
  { path: '/sponsor/campaign-request/:ID', name: 'CreateAdRequest', component: CreateAdRequest },
  { path: '/sponsor/request-update/:ID', name: 'UpdateRequest', component: UpdateRequest },

  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard },

  { path: '/influencer/dashboard', name: 'InfluencerDashboard', component: InfluencerDashboard },
  { path: '/influencer/profile', name: 'InfluencerProfile', component: InfluencerProfile },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  export default router;
