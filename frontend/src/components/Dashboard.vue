<template>
    <div class="dashboard">
        <EntityFormModal
            v-if="currentFormType"
            :is-visible="isModalVisible"
            :form-config="currentFormConfig"
            :baseURL="currentBaseURL"
            :edit-data="currentEditData"
            @close="isModalVisible = false"
            @success="handleSuccessCreation"
        />
        <div class="dashboard-header">
            <h1 class="dashboard-title">Welcome, {{ userRole.toUpperCase() }}!</h1>
            <button @click="logout" class="logout-btn">Logout</button>

            <div v-if="userRole === 'admin' || userRole === 'teacher'" class="data-grid">
            </div>

            <hr>

            <div class="details-section">
                <TeacherList v-if="userRole ==='admin'" @data-loaded="updateData" @open-create="openModal('teacher')" @open-edit="openModal('teacher', $event)"/>
                <StudentList v-if="userRole === 'admin' || userRole === 'teacher'" :class-map="classMap" @data-loaded="updateData" @open-create="openModal('student')" @open-edit="openModal('student', $event)"/>

                <div v-if="userRole === 'student'">
                    <h3>This is the Student Dashboard. You can view your classes and grades here.</h3>
                </div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card teacher-card">
                <div class="stat-icon">👨‍🏫</div>
                <div class="stat-content">
                    <h2>{{ teachers.length }}</h2>
                    <p>Teachers</p>
                </div>
            </div>
            <div class="stat-card class-card">
                <div class="stat-icon">📚</div>
                <div class="stat-content">
                    <h2>{{ classes.length }}</h2>
                    <p>Classes</p>
                </div>
            </div>
            <div class="stat-card student-card">
                <div class="stat-icon">👨‍🎓</div>
                <div class="stat-content">
                    <h2>{{ students.length }}</h2>
                    <p>Students</p>
                </div>
            </div>
        </div>

        <div class="content-section">
            <div class="data-lists">
                <template v-if="userRole === 'admin'">
                    <TeacherList 
                    @data-loaded="updateData"
                    @open-create="openModal('teacher')"
                    @open-edit="openModal('teacher', $event)"
                    />

                    <ClassList 
                        :teacher-map="teacherMap" 
                        @data-loaded="updateData" 
                        @open-create="openModal('class')" 
                        @open-edit="openModal('class', $event)"
                    />

                    <StudentList 
                        :class-map="classMap" 
                        @data-loaded="updateData" 
                        @open-create="openModal('student')" 
                        @open-edit="openModal('student', $event)"
                    />
                </template>

                <template v-else-if="userRole === 'teacher'">
                    <ClassList 
                        :teacher-map="teacherMap" 
                        @data-loaded="updateData" 
                        @open-create="openModal('class')" 
                        @open-edit="openModal('class', $event)"
                    />
                    <StudentList
                        :class-map="classMap"
                        @data-loaded="updateData"
                        @open-create="openModal('student')"
                        @open-edit="openModal('student', $event)"
                    />
                </template>

                <template v-else-if="userRole === 'student'">
                    <div class="student-view-placeholder">
                        <p>Anda login sebagai **Siswa**. Anda hanya dapat melihat informasi terkait mata pelajaran dan nilai Anda.</p>
                        </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import TeacherList from './TeacherList.vue';
import ClassList from './ClassList.vue';
import StudentList from './StudentList.vue';
import EntityFormModal from './FormModal.vue';

const BASE_URL = 'http://127.0.0.1:8000/api/';

export default {
    name: 'Dashboard',
    components: {
        TeacherList,
        ClassList,
        StudentList,
        EntityFormModal
    },
    data() {
        return {
            teachers: [],
            classes: [],
            students: [],
            isModalVisible: false,
            currentFormType: null,
            currentEditData: null,
        };
    },
    computed: {
        userRole() {
            return localStorage.getItem('user_role') || 'guest';
        },
        // membuat map Teacher, Class dan Student untuk ClassList
        teacherMap() {
            return this.teachers.reduce((map, teacher) => {
                map[teacher.id] = teacher.name;
                return map;
            }, {});
        },
        classMap() {
            return this.classes.reduce((map, cls) => {
                map[cls.id] = cls.name;
                return map;
            }, {});
        },
        currentFormConfig() {
            return this.getFormConfig(this.currentFormType);
        },
        currentBaseURL() {
            if (this.currentFormType === 'teacher') return BASE_URL + 'teachers/';
            if (this.currentFormType === 'class') return BASE_URL + 'classes/';
            if (this.currentFormType === 'student') return BASE_URL + 'students/';
            return '';
        }
    },
    mounted() {
        this.fetchDashboardData();
    },
    methods: {
        updateData(payload) {
            if (payload.module === 'teachers') {
                this.teachers = payload.data;
            } else if (payload.module === 'classes') {
                this.classes = payload.data;
            } else if (payload.module === 'students') {
                this.students = payload.data;
            }
        },

        async fetchDashboardData() {
            try {
                const [teachersRes, classesRes, studentsRes] = await Promise.all([
                    fetch(BASE_URL + 'teachers/'),
                    fetch(BASE_URL + 'classes/'),
                    fetch(BASE_URL + 'students/')
                ]);
                this.teachers = await teachersRes.json();
                this.classes = await classesRes.json();
                this.students = await studentsRes.json();
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                if (error.response && error.response.status === 401) {
                    this.logout();
                }
            }
        },
        handleSuccessCreation() {
            this.fetchDashboardData();
        },
        openModal(type, editData = null) {
            this.currentFormType = type;
            this.currentEditData = editData;
            this.isModalVisible = true;
        },
        logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user_role');
            this.$router.push('/login');
        },
        getFormConfig(type) {
            switch (type) {
                case 'teacher':
                return {
                    title: 'Guru',
                    fields: {
                        name: { label: 'Nama', type: 'text', placeholder: 'Nama Guru' },
                        subject: { label: 'Mata Pelajaran', type: 'text', placeholder: 'Misal: Matematika' },
                    }
                };
            case 'class':
                return {
                    title: 'Kelas',
                    fields: {
                        name: { label: 'Nama Kelas', type: 'text', placeholder: 'Misal: Kelas 10-A' },
                        teacher_id: { // Nama field harus sesuai dengan Serializer DRF
                            label: 'Guru Pengajar', 
                            type: 'select', 
                            options: this.teachers.filter(t => !t.deleted) // Hanya tampilkan guru yang aktif
                        },
                    }
                };
            case 'student':
                return {
                    title: 'Siswa',
                    fields: {
                        name: { label: 'Nama Siswa', type: 'text', placeholder: 'Nama Siswa' },
                        age: { label: 'Usia', type: 'number', placeholder: '15' },
                        class_assigned_id: { // Nama field harus sesuai dengan Serializer DRF
                            label: 'Kelas',
                            type: 'select',
                            options: this.classes.filter(c => !c.deleted)
                        },
                    }
                };
            default:
                return {};
        }
    }
},
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-title {
  color: white;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  margin: 0;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: white;
  color: #667eea;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.2);
}

.stat-icon {
  font-size: 3rem;
  margin-right: 20px;
}

.stat-content h2 {
  font-size: 2.5rem;
  margin: 0;
  font-weight: bold;
}

.stat-content p {
  margin: 5px 0 0 0;
  color: #666;
  font-size: 1.1rem;
  font-weight: 500;
}

.teacher-card .stat-icon { color: #42b983; }
.class-card .stat-icon { color: #3498db; }
.student-card .stat-icon { color: #e67e22; }

.content-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.data-lists {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard {
    padding: 15px;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .dashboard-title {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .stat-card {
    padding: 20px;
  }

  .stat-icon {
    font-size: 2.5rem;
  }

  .stat-content h2 {
    font-size: 2rem;
  }

  .data-lists {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .content-section {
    padding: 20px;
  }
}
</style>