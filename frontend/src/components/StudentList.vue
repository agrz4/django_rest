<template>
    <div class="list-container student-list">
        <h4>Students Lists ({{ students.length }})</h4>

        <button @click="openCreateForm" class="btn btn-create">
            + Add Student
        </button>

        <ul v-if="!loading && !error">
            <li v-for="student in students" :key="student.id" :class="{ 'deleted-item': student.deleted }">
                <span class="student-info">
                {{ student.name }} ({{ student.age }} tahun) - Kelas: {{ getClassId(student.class_assigned) }}
                <span v-if="student.deleted" class="deleted-tag">🗑️</span>
                </span>

                <div class="actions">
                    <button
                    @click="softDelete(student.id)"
                    :disabled="student.deleted"
                    :class="{'btn-delete': !student.deleted, 'btn-disabled': student.deleted}">
                        {{ student.deleted ? 'Deleted' : 'Soft Delete' }}
                    </button>

                    <button class="btn-update" @click="openEditForm(student)">Edit</button>
                </div>
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
    classMap: { type: Object, required: true }
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
          // Emit data-loaded agar Dashboard dapat memperbarui state students
          this.$emit('data-loaded', { module: 'students', data: response.data });
        })
        .catch(error => {
          console.error("Gagal mengambil data Siswa:", error);
          this.error = 'Gagal memuat Siswa.';
          this.loading = false;
        });
    },

        // method CRUD
        openCreateForm() {
            this.$emit('open-create');
        },
        openEditForm(student) {
            this.$emit('open-edit', student);
        },
        async softDelete(id) {
            if (!confirm(`You sure to soft delete Student ID ${id}?`)) {
                return;
            }

            try {
                await axios.delete(API_URL + `${id}/`);

                alert(`Student ID ${id} successfully deleted.`);
                this.fetchStudents();

            } catch (error) {
                console.error("Failed to soft delete:", error.response || error);
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
/* Style tambahan */
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