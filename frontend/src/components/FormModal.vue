<template>
    <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
            <h3>{{ editData ? 'Edit' : 'Add' }} {{ formConfig.title }}</h3>

            <form @submit.prevent="submitForm">
                <div v-for="(field, key) in formConfig.fields" :key="key" class="form-group">
                    <label :for="key">{{ field.label }}:</label>

                    <input
                    v-if="field.type === 'text' || field.type === 'number'"
                    :type="field.type"
                    :id="key"
                    v-model="formData[key]"
                    required
                    :placeholder="field.placeholder"
                    >

                    <select
            v-else-if="field.type === 'select'"
            :id="key"
            v-model="formData[key]"
            required
          >
            <option value="" disabled>Select {{ field.label }}</option>
            <option v-for="option in field.options" :key="option.id" :value="option.id">
              {{ option.name }}
            </option>
          </select>
            </div>

            <div class="form-actions">
          <button type="submit" :disabled="isSubmitting">{{ isSubmitting ? 'Process...' : (editData ? 'Update' : 'Save') }}</button>
          <button type="button" @click="closeModal" class="btn-cancel">Cancel</button>
        </div>

        <p v-if="submissionError" class="error-message">Failed: {{ submissionError }}</p>

            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'EntityFormModel',
    props: {
        isVisible: { type: Boolean, required: true },
        formConfig: { type: Object, required: true},
        baseURL: { type: String, required: true },
        editData: { type: Object, default: null },
    },
    data() {
        return {
            formData: {},
            isSubmitting: false,
            submissionError: null,
        };
    },
    watch: {
        isVisible(newVal) {
            if (newVal) {
                this.resetForm();
            }
        }
    },
    methods: {
        resetForm() {
            this.formData = Object.keys(this.formConfig.fields).reduce((acc, key) => {
                acc[key] = this.editData ? this.editData[key] || '' : '';
                if (this.formConfig.fields[key].type === 'number') {
                    acc[key] = this.editData ? this.editData[key] || null : null;
                }
                return acc;
            }, {});
            this.submissionError = null;
        },
        closeModal() {
            this.$emit('close');
        },
        async submitForm() {
            this.isSubmitting = true;
            this.submissionError = null;

            try {
                const payload = this.preparePayload();

                let response;
                if (this.editData) {
                    response = await axios.put(`${this.baseURL}${this.editData.id}/`, payload);
                    alert(`${this.formConfig.title} successfully updated!`);
                } else {
                    response = await axios.post(this.baseURL, payload);
                    alert(`${this.formConfig.title} successfully added!`);
                }

                this.$emit('success');
                this.closeModal();
            } catch (error) {
                console.error(`Failed to ${this.editData ? 'update' : 'add'} ${this.formConfig.title}:`, error.response.data);
                this.submissionError = this.formatError(error.response.data);
            } finally {
                this.isSubmitting = false;
            }
        },
        preparePayload() {
            // Membersihkan payload dari nilai null/kosong jika tidak diperlukan
            const payload = Object.keys(this.formData).reduce((acc, key) => {
                const value = this.formData[key];
                if (value !== '' && value !== null) {
                    acc[key] = value;
                }
                return acc;
            }, {});

            // Convert number fields to integers
            if (payload.age) {
                payload.age = parseInt(payload.age);
            }

            return payload;
        },
        formatError(errors) {
            if (typeof errors == 'object') {
                return Object.keys(errors).map(key => {
                const fieldName = key.charAt(0).toUpperCase() + key.slice(1);
                return `${fieldName}: ${errors[key].join(' ')}`;
                }).join('; ');
            }
            return 'Unformatted error.';
        }
    }
};
</script>

<style scoped>
/* --- Styles Modal --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
h3 { margin-top: 0; color: #34495e; }

/* --- Form Styles --- */
.form-group {
  margin-bottom: 15px;
  text-align: left;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
input[type="text"], input[type="number"], select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #42b983;
  color: white;
}
.btn-cancel {
  background-color: #ccc;
}
.error-message {
  color: #e74c3c;
  margin-top: 15px;
  border: 1px solid #e74c3c;
  padding: 10px;
  border-radius: 4px;
  background-color: #fceae9;
}
</style>