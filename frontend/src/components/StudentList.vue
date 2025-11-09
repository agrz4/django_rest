<template>
    <div class="list-container student-list">
        <h4>Students Lists ({{ students.length }})</h4>

        <button v-if="canManage" @click="openCreateForm" class="btn btn-create">
            + Add Student
        </button>

        <p v-if="loading">Loading student data...</p>
        <p v-if="error">{{ error }}</p>

        <ul v-else>
            <li v-for="student in students" :key="student.id" :class="{ 'deleted-item': student.deleted }">
                <span class="student-info">
                {{ student.name }} ({{ student.age }} tahun) - Kelas: {{ getClassId(student.class_assigned) }}
                <span v-if="student.deleted" class="deleted-tag">🗑️</span>
                </span>

                <div v-if="canManage" class="actions">
                    <button
                    @click="softDelete(student.id)"
                    :disabled="student.deleted"
                    :class="{'btn-delete': !student.deleted, 'btn-disabled': student.deleted}">
                        {{ student.deleted ? 'Deleted' : 'Soft Delete' }}
                    </button>

                    <button class="btn-update" @click="openEditForm(student)" :disabled="student.deleted">Edit</button>
                </div>
                <div v-else-if="student.deleted" class="actions">
                    <span class="deleted-tag">Status: Deleted</span>
                </div>
            </li>
        </ul>

    </div>
</template>

<script>
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/students/';
const CLASS_API_URL = 'http://127.0.0.1:8000/api/classes/'; // Diperlukan untuk form

export default {
    name: 'StudentList',
    props: {
        classMap: { type: Object, required: true }
    },
    data() {
        return {
            students: [],
            classes: [], // Diperlukan untuk opsi select di form
            loading: true,
            error: null
        };
    },
    // Tambahkan Computed Property untuk Kontrol Akses
    computed: {
        canManage() {
            // Admin dan Teacher diizinkan untuk melihat dan memanipulasi daftar siswa.
            const role = localStorage.getItem('user_role');
            return role === 'admin' || role === 'teacher';
        }
    },
    mounted() {
        this.fetchStudents();
        // Karena komponen ini mungkin memanggil modal, kita perlu fetch data FK juga.
        this.fetchClassesForForm(); 
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
                    console.error("Gagal mengambil data Siswa:", error.response || error);
                    this.error = 'Failed to load student data. Access Denied or Token Expired.';
                    this.loading = false;
                });
        },
        fetchClassesForForm() {
            // Mengambil daftar kelas untuk mengisi opsi dropdown di form (jika modal dipicu)
            axios.get(CLASS_API_URL)
                .then(response => {
                    this.classes = response.data;
                })
                .catch(error => {
                    console.error("Failed to get class data for form:", error);
                });
        },

        // method CRUD
        openCreateForm() {
            if (this.canManage) {
                // Tambahkan data FK yang diperlukan ke emit
                this.$emit('open-create'); 
            }
        },
        openEditForm(student) {
             if (this.canManage && !student.deleted) {
                this.$emit('open-edit', student);
            }
        },
        async softDelete(id) {
            if (!this.canManage || !confirm(`You sure to soft delete Student ID ${id}?`)) {
                return;
            }

            try {
                await axios.delete(API_URL + `${id}/`);

                alert(`Student ID ${id} successfully deleted.`);
                this.fetchStudents();

            } catch (error) {
                console.error("Failed to soft delete:", error.response || error);
                alert("Failed to soft delete. Check console for details.");
            }
        },

        // --- Helper ---
        getClassId(classId) {
            return this.classMap[classId] || 'ID: ' + classId;
        }
    }
};
</script>

<style scoped>
/* (Style Anda yang sudah ada di sini...) */
.list-container { padding: 15px; }
ul { padding: 0; }
li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px dotted #eee;
}
.student-info { flex-grow: 1; }
.actions button {
    margin-left: 5px;
    padding: 5px 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}
.btn-create {
    background-color: #42b983;
    color: white;
    margin-bottom: 15px;
    padding: 8px 15px;
}
.btn-delete { background-color: #e74c3c; color: white; }
.btn-update { background-color: #f39c12; color: white; }
.btn-disabled { background-color: #bdc3c7; cursor: not-allowed; color: #666; }

.deleted-item { text-decoration: line-through; color: #a0a0a0; }
.deleted-tag { color: red; font-weight: bold; }
</style>