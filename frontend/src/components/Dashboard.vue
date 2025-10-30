<template>
    <div class="dashboard">
        <div v-if="loading" class="loading">
            <p>Load all data from API...</p>
        </div>
        <div v-else-if="error" class="error">
            <p>Failed to load dashboard: {{ error }}</p>
        </div>

        <div v-else class="data-grid">
            <div class="summary-box teacher-box">
                <h3>Active Teacher ({{ teachers.length }})</h3>
                <p>Total Teacher.</p>
            </div>

            <div class="summary-box class-box">
                <h3>Active Class ({{ classes.length }})</h3>
                <p>Total Class.</p>
            </div>

            <div class="summary-box student-box">
                <h3>Active Student ({{ students.length }})</h3>
                <p>Total Student.</p>
            </div>
        </div>

        <div class="details-section">
            <div class="list-container teacher-list">
                <h4>Teacher List (Active)</h4>
                <ul>
                    <li v-for="teacher in teachers" :key="teacher.id" :class="{ 'deleted-item': teacher.deleted }">
                        {{ teacher.name }} ({{ teacher.subject }})
                        <span v-if="teacher.deleted" class="deleted-tag">🗑️</span>
                    </li>
                </ul>
            </div>

            <div class="list-container class-list">
                <h4>Class List</h4>
                <ul>
                    <li v-for="cls in classes" :key="cls.id">
                        {{ cls.name }} diajar oleh <strong>{{ getTeacherName(cls.teacher) }}</strong>
                    </li>
                </ul>
            </div>

            <div class="list-container student-list">
                <h4>Student List</h4>
                <ul>
                    <li v-for="student in students" :key="student.id">
                        {{ student.name }} ({{ student.age }} tahun) - Kelas: <strong>{{ getClassId(student.class_assigned) }}</strong>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/';

export default {
    name: 'Dashboard',
    data() {
        return {
            teachers: [],
            classes: [],
            students: [],
            loading: true,
            error: null
        };
    },

    computed: {
        teacherMap() {
            return this.teachers.reduce((map, teacher) => {
                map[teacher.id] = teacher.name;
                return map;
            }, {});
        }
    },
    mounted() {
        console.log('Dashboard component mounted');
        this.fetchDashboardData();
    },
    methods: {
        fetchDashboardData() {
            console.log('Starting to fetch dashboard data...');
            console.log('BASE_URL:', BASE_URL);

            const teacherPromise = axios.get(BASE_URL + 'teachers/');
            const classPromise = axios.get(BASE_URL + 'classes/');
            const studentPromise = axios.get(BASE_URL + 'students/');

            console.log('Making API calls to:', BASE_URL + 'teachers/', BASE_URL + 'classes/', BASE_URL + 'students/');

            // Mengambil semua data secara paralel
            Promise.all([teacherPromise, classPromise, studentPromise])
            .then(responses => {
                console.log('API responses received:', responses);
                console.log('Teachers data:', responses[0].data);
                console.log('Classes data:', responses[1].data);
                console.log('Students data:', responses[2].data);

                this.teachers = responses[0].data;
                this.classes = responses[1].data;
                this.students = responses[2].data;
                this.loading = false;

                console.log('Data loaded successfully. Teachers:', this.teachers.length, 'Classes:', this.classes.length, 'Students:', this.students.length);
            })
            .catch(err => {
                console.error("Failed get data dashboard:", err);
                console.error("Error details:", err.response || err.message);
                this.error = "An error occurred while contacting the API. Check the console.";
                this.loading = false;
            });
        },
        // Metode helper untuk mendapatkan nama guru dari ID dan ID Kelas
        getTeacherName(teacherId) {
            return this.teacherMap[teacherId] || 'Unknown';
        },
        getClassId(classId) {
            const cls = this.classes.find(c => c.id === classId);
            return cls ? cls.name : 'ID: ' + classId;
        }
    }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.data-grid {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
}
.details-section {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  text-align: left;
}
.list-container {
  flex: 1;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.list-container ul {
  list-style-type: none;
  padding: 0;
}
.list-container li {
  padding: 5px 0;
  border-bottom: 1px dotted #eee;
}

/* Summary Box Styling */
.summary-box {
  flex: 1;
  margin: 10px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: white;
}
.teacher-box { background-color: #42b983; }
.class-box { background-color: #3498db; }
.student-box { background-color: #e67e22; }

/* Status Styling */
.deleted-item {
    text-decoration: line-through;
    color: #a0a0a0;
}
.deleted-tag {
    color: red;
    font-weight: bold;
}
.loading, .error {
    padding: 20px;
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
}
</style>