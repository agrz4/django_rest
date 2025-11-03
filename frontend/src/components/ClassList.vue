<template>
    <div class="list-container class-list">
        <h4>Class List ({{ classes.length }})</h4>

        <button @click="openCreateForm" class="btn btn-create">
            + Add Class
        </button>

        <ul v-if="!loading && !error">
            <li v-for="cls in classes" :key="cls.id" :class="{ 'deleted-item': cls.deleted }">
                <span class="class-info">
                {{ cls.name }} Diajar oleh {{ getTeacherName(cls.teacher) }}
                <span v-if="cls.deleted" class="deleted-tag">🗑️</span>
                </span>

                <div class="actions">
                    <button
                    @click="softDelete(cls.id)"
                    :disabled="cls.deleted"
                    :class="{'btn-delete': !cls.deleted, 'btn-disabled': cls.deleted}">
                        {{ cls.deleted ? 'Deleted' : 'Soft Delete' }}
                    </button>

                    <button class="btn-update" @click="openEditForm(cls)">Edit</button>
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
    teacherMap: { type: Object, required: true }
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
          // Emit data-loaded to update Dashboard's teacherMap
          this.$emit('data-loaded', { module: 'classes', data: response.data });
        })
        .catch(error => {
          console.error("Failed to fetch classes:", error);
          this.error = 'Failed to load classes.';
          this.loading = false;
        });
    },

        // method CRUD
        openCreateForm() {
            this.$emit('open-create');
        },
        openEditForm(cls) {
            this.$emit('open-edit', cls);
        },
        async softDelete(id) {
            if (!confirm(`You sure to soft delete Class ID ${id}?`)) {
                return;
            }

            try {
                await axios.delete(API_URL + `${id}/`);

                alert(`Class ID ${id} successfully deleted.`);
                this.fetchClasses();

            } catch (error) {
                console.error("Failed to soft delete:", error.response || error);
            }
        },

        // --- Helper ---
        getTeacherName(teacherId) {
          // teacherId is already the teacher name from the API
          return teacherId || 'Unknown';
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