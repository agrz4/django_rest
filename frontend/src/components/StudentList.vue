<template>
    <div class="list-container student-list">
        <h4>Students Lists ({{ students.length }})</h4>
        <ul v-if="!loading && !error">
            <li v-for="student in students" :key="student.id">
                {{ student.name }} ({{ student.age }} tahun) - Kelas: {{ getClassId(student.class_assigned) }}
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/students/';

export default {
    name: 'StudentList',
    props: {
        // Menerima map class dari Dashboard
        classMap: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            students: [],
            loading: true,
            error: null
        };
    },
    mounted() {
        this.fetchStudents();
    },
    methods: {
        fetchStudents() {
            axios.get(API_URL)
            .then(response => {
                this.students = response.data;
                this.loading = false;
                this.$emit('data-loaded', { module: 'students', data: response.data });
            })
            .catch(error => {
                console.error("Failed to get data Student:", error);
                this.error = 'Failed to load students.';
                this.loading = false;
            });
        },
        getClassId(classId) {
            return this.classMap[classId] || 'ID: ' + classId;
        }
    }
};
</script>

<style scoped>
.list-container { border: 1px solid #ccc; border-radius: 8px; padding: 15px; }
ul { list-style-type: none; padding: 0; }
li { padding: 5px 0; border-bottom: 1px dotted #eee; text-align: left; }
h4 { text-align: center; }
</style>