<template>
    <div class="list-container class-list">
        <h4>Class List ({{ classes.length }})</h4>

        <button v-if="canManage" @click="openCreateForm" class="btn btn-create">
            + Add Class
        </button>

        <p v-if="loading">Loading class data...</p>
        <p v-if="error">{{ error }}</p>

        <ul v-else>
            <li v-for="cls in classes" :key="cls.id" :class="{ 'deleted-item': cls.deleted }">
                <span class="class-info">
                {{ cls.name }} Diajar oleh **{{ getTeacherName(cls.teacher) }}**
                <span v-if="cls.deleted" class="deleted-tag">🗑️</span>
                </span>

                <div v-if="canManage" class="actions">
                    <button
                    @click="softDelete(cls.id)"
                    :disabled="cls.deleted"
                    :class="{'btn-delete': !cls.deleted, 'btn-disabled': cls.deleted}">
                        {{ cls.deleted ? 'Deleted' : 'Soft Delete' }}
                    </button>

                    <button class="btn-update" @click="openEditForm(cls)" :disabled="cls.deleted">Edit</button>
                </div>
                <div v-else-if="cls.deleted" class="actions">
                    <span class="deleted-tag">Status: Deleted</span>
                </div>
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
        // Digunakan untuk mendapatkan nama guru di tampilan list
        teacherMap: { type: Object, required: true }
    },
    data() {
        return {
            classes: [],
            loading: true,
            error: null
        };
    },
    // Tambahkan Computed Property untuk Kontrol Akses
    computed: {
        canManage() {
            // Admin dan Teacher diizinkan untuk mengelola Kelas.
            const role = localStorage.getItem('user_role');
            return role === 'admin' || role === 'teacher';
        }
    },
    mounted() {
        this.fetchClasses();
    },
    methods: {
        fetchClasses() {
            // Menggunakan Axios untuk memanfaatkan Interceptor JWT
            axios.get(API_URL)
                .then(response => {
                    this.classes = response.data;
                    this.loading = false;
                    this.$emit('data-loaded', { module: 'classes', data: response.data });
                })
                .catch(error => {
                    console.error("Failed to fetch classes:", error.response || error);
                    this.error = 'Failed to load classes. Access Denied or Token Expired.';
                    this.loading = false;
                });
        },

        // method CRUD
        openCreateForm() {
            if (this.canManage) {
                this.$emit('open-create');
            }
        },
        openEditForm(cls) {
            if (this.canManage && !cls.deleted) {
                this.$emit('open-edit', cls);
            }
        },
        async softDelete(id) {
            if (!this.canManage || !confirm(`You sure to soft delete Class ID ${id}?`)) {
                return;
            }

            try {
                // Mengirim request DELETE
                await axios.delete(API_URL + `${id}/`);

                alert(`Class ID ${id} successfully deleted.`);
                this.fetchClasses();

            } catch (error) {
                console.error("Failed to soft delete:", error.response || error);
                alert("Failed to soft delete. Check console for details.");
            }
        },

        // --- Helper ---
        getTeacherName(teacherId) {
            // Menggunakan teacherMap dari props untuk resolusi nama Guru
            return this.teacherMap[teacherId] || 'Unknown';
        }
    }
};
</script>

<style scoped>
/* Style Anda yang sudah ada */
.list-container { padding: 15px; }
ul { padding: 0; }
li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px dotted #eee;
}
.class-info { flex-grow: 1; }
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