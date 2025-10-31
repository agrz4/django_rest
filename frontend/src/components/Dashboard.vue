<template>
    <div class="dashboard">
        <div class="data-grid">
            <div class="summary-box teacher-box">
                <h3>Teacher ({{ teachers.length }})</h3>
            </div>
            <div class="summary-box class-box">
                <h3>Class ({{ classes.length }})</h3>
            </div>
            <div class="summary-box student-box">
                <h3>Student ({{ students.length }})</h3>
            </div>
        </div>

        <hr>

        <div class="details-section">
            <TeacherList @data-loaded="updateData"/>

            <ClassList :teacher-map="teacherMap" @data-loaded="updateData"/>

            <StudentList :class-map="classMap" @data-loaded="updateData"/>
        </div>
    </div>
</template>

<script>
import TeacherList from './TeacherList.vue';
import ClassList from './ClassList.vue';
import StudentList from './StudentList.vue';

export default {
    name: 'Dashboard',
    components: {
        TeacherList,
        ClassList,
        StudentList
    },
    data() {
        return {
            teachers: [],
            classes: [],
            students: [],
        };
    },
    computed: {
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
        }
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
        }
    }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
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
</style>