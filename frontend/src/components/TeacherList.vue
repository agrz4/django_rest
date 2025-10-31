<template>
    <div class="list-container teacher-list">
        <h4>Teachers List ({{ teachers.length }})</h4>
        <ul v-if="!loading && !error">
            <li v-for="teacher in teachers" :key="teacher.id" :class="{ 'deleted-item': teacher.deleted }">
                {{ teacher.name }} ({{ teacher.subject }})
                <span v-if="teacher.deleted" class="deleted-tag">🗑️</span>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/teachers/';

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
            axios.get(API_URL)
            .then(response => {
                this.teachers = response.data;
                this.loading = false;
                // mengirim data ke komponen Dashboard melalui event
                this.$emit('data-loaded', { module: 'teachers', data: response.data });
            })
            .catch(error => {
                console.error("Failed to get teacher data: ", error);
                this.error = 'Failed to load teacher.';
                this.loading = false;
            });
        }
    }
};
</script>

<style scoped>

.list-container {
  /* Style akan dikontrol di Dashboard.vue */
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
}
ul { list-style-type: none; padding: 0; }
li { padding: 5px 0; border-bottom: 1px dotted #eee; text-align: left; }
.deleted-item { text-decoration: line-through; color: #a0a0a0; }
.deleted-tag { color: red; font-weight: bold; }
h4 { text-align: center; }
</style>