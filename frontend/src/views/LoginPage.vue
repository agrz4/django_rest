<template>
    <div>
        <h2>Login School System</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit" :disabled="isLoading">
                {{ isLoading ? 'Process...' : 'Login' }}
            </button>
        </form>
        <p v-if="error" class="error-message">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const LOGIN_URL = 'http://127.0.0.1:8000/api/token/';

export default {
    name:'LoginPage',
    data() {
        return {
            username: '',
            password: '',
            isLoading: false,
            error: null,
        };
    },
    methods: {
        async handleLogin() {
            this.isLoading = true;
            this.error = null;

            try {
                console.log('Attempting login with:', { username: this.username, password: this.password });
                const response = await axios.post(LOGIN_URL, {
                    username: this.username,
                    password: this.password,
                });
                console.log('Login response:', response);

                const { access, refresh } = response.data;

                // Decoded Access Token untuk mendapatkan role
                const decodedToken = jwtDecode(access);
                const userRole = decodedToken.role;
                console.log('Decoded token:', decodedToken);
                console.log('User role:', userRole);

                localStorage.setItem('access_token', access);
                localStorage.setItem('refresh_token', refresh);
                localStorage.setItem('user_role', userRole);

                this.$router.push('/');
            } catch (err) {
                console.error("Login Fail:", err.response);
                if (err.response) {
                    if (err.response.status === 401) {
                        this.error = "Invalid username or password.";
                    } else if (err.response.data) {
                        this.error = err.response.data.detail || err.response.data.message || 'Login failed';
                    } else {
                        this.error = 'Login failed';
                    }
                } else {
                    this.error = err.message || 'Network error';
                }
            } finally {
                this.isLoading = false;
            }
        },
    },
};
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f4f7f6;
}
.login-card {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 380px;
    text-align: center;
}
.form-group {
    margin-bottom: 20px;
    text-align: left;
}
label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}
input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
}
button {
    width: 100%;
    padding: 12px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}
.error-message {
    color: #e74c3c;
    margin-top: 15px;
    padding: 10px;
    border: 1px solid #e74c3c;
    border-radius: 5px;
    background-color: #fceae9;
}
</style>