<template>
    <div class="list-container class-list">
        <h4>Class List ({{ classes.length }})</h4>
        <ul v-if="!loading && !error">
            <li v-for="cls in classes" :key="cls.id">
                {{ cls.name }} Diajar Oleh {{ getTeacherName(cls.teacher) }}
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/classes/';

export default {
    name: 'ClassList',
    props: {
        // menerima map Teacher dari Dashboard
        teacherMap: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            classes: [],
            loading: true,
            error: null
        };
    },
    mounted() {
        this.fetchClasses();
    },
    methods: {
        fetchClasses() {
            axios.get(API_URL)
            .then(response => {
                this.classes = response.data;
                this.loading = false;
                this.$emit('data-loaded', { module: 'classes', data: response.data });
            })
            .catch(error => {
                console.error("Failed to get class data:", error);
                this.error = 'Failed to load Class.';
                this.loading = false;
            });
        },
        getTeacherName(teacherId) {
            return this.teacherMap[teacherId] || 'Unknown';
        }
    }
}
</script>

<style scoped>
.list-container { border: 1px solid #ccc; border-radius: 8px; padding: 15px; }
ul { list-style-type: none; padding: 0; }
li { padding: 5px 0; border-bottom: 1px dotted #eee; text-align: left; }
h4 { text-align: center; }
</style>