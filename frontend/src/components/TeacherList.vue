<template>
    <div class="list-container teacher-list">
        <h4>Teachers List ({{ teachers.length }})</h4>

        <button v-if="canManage" @click="openCreateForm" class="btn btn-create">
            + Add Teacher
        </button>

        <p v-if="loading">Loading teacher data...</p>
        <p v-if="error">{{ error }}</p>

        <ul v-else>
            <li v-for="teacher in teachers" :key="teacher.id" :class="{ 'deleted-item': teacher.deleted }">
                <span class="teacher-info">
                    {{ teacher.name }} ({{ teacher.subject }})
                <span v-if="teacher.deleted" class="deleted-tag">🗑️</span>
                </span>

                <div v-if="canManage" class="actions">
                    <button
                        @click="softDelete(teacher.id)"
                        :disabled="teacher.deleted"
                        :class="{'btn-delete': !teacher.deleted, 'btn-disabled': teacher.deleted}">
                        {{ teacher.deleted ? 'Deleted' : 'Soft Delete' }}
                    </button>
                    
                    <button class="btn-update" @click="openEditForm(teacher)" :disabled="teacher.deleted">Edit</button>
                </div>
                <div v-else-if="teacher.deleted" class="actions">
                    <span class="deleted-tag">Status: Deleted</span>
                </div>
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

    // tambah computer property untuk kontrol akses
    computed: {
        canManage() {
            const role = localStorage.getItem('user_role');
            return role === 'admin';
        }
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
        },

        // method CRUD
        openCreateForm() {
            if (this.canManage) {
                this.$emit('open-create');
            }
        },
        openEditForm(teacher) {
            if (this.canManage && !teacher.deleted) {
                this.$emit('open-edit', teacher);
            }
        },
        async softDelete(id) {
            if (!this.canManage || !confirm(`You sure to soft delete Teacher ID ${id}?`)) {
                return;
            }

            try {
                await axios.delete(API_URL + `${id}/`);

                alert(`Teacher ID ${id} successfully deleted.`);
                this.fetchTeachers();

            } catch (error) {
                console.error("Failed to soft delete:", error.response || error);
            }
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
.teacher-info { flex-grow: 1; }
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