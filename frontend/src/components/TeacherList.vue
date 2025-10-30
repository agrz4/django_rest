<template>
    <div class="teacher-list">
        <h2>List Teacher</h2>
        <p v-if="loading">Loading...</p>
        <p v-if="error">{{  error }}</p>

        <ul v-if="!loading && !error">
            <li v-for="teacher in teachers" :key="teacher.id">
                <strong>Nama:</strong> {{ teacher.name }} ({{ teacher.subject }})
                <span v-if="teacher.deleted" style="color: red;">- Soft Delete</span>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'TeacherList',
    data() {
        return {
            teachers: [],
            loading: true,
            error: null
        };
    },
    mounted() {
        this.fetchTeachers();
    },
    methods: {
        fetchTeachers() {
            const API_URL = 'http://127.0.0.1:8000/api/teachers/';

            axios.get(API_URL)
            .then(response => {
                this.teachers = response.data;
                this.loading = false;
            })
            .catch(error => {
                console.error("Failed to get teacher data:", error);
                this.error = 'Failed to load data from API';
                this.loading = false;
            });
        }
    }
};
</script>

<style scoped>
.teacher-list {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 10px 0;
  padding: 5px;
  border-bottom: 1px dashed #eee;
}
</style>