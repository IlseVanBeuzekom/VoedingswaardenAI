<!-- frontend/src/components/forms/DailyFoodEntryForm.vue -->
<template>
  <div class="entry-form">
    <h4>{{ mode === 'edit' ? 'Item Bewerken' : 'Item Toevoegen' }}</h4>
    
    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-row">
        <div class="form-group">
          <label for="type">Type</label>
          <select v-model="form.type" id="type" class="form-input" @change="resetSelection">
            <option value="product">Product</option>
            <option value="recipe">Recept</option>
          </select>
        </div>

        <div class="form-group">
          <label for="amount">Hoeveelheid</label>
          <input
            v-model.number="form.amount"
            type="number"
            step="0.1"
            min="0.1"
            id="amount"
            required
            class="form-input"
            placeholder="0"
          />
        </div>

        <div class="form-group">
          <label for="unit">Eenheid</label>
          <select v-model="form.unit" id="unit" class="form-input">
            <option value="gram">gram</option>
            <option value="kg">kg</option>
            <option value="ml">ml</option>
            <option value="liter">liter</option>
            <option value="stuk">stuk</option>
            <option value="el">eetlepel</option>
            <option value="tl">theelepel</option>
            <option value="kopje">kopje</option>
            <option value="portie" v-if="form.type === 'recipe'">portie</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label for="item">{{ form.type === 'product' ? 'Product' : 'Recept' }}</label>
        <select 
          v-model="form.selectedId" 
          id="item" 
          class="form-input"
          required
        >
          <option value="">Kies {{ form.type === 'product' ? 'product' : 'recept' }}</option>
          <option 
            v-for="item in availableItems" 
            :key="item.id" 
            :value="item.id"
          >
            {{ item.name }} 
            <span v-if="form.type === 'recipe'">
              ({{ item.servings }} pers, {{ item.preparation_time }} min)
            </span>
          </option>
        </select>
      </div>

      <div class="form-actions">
        <BaseButton type="submit" :disabled="!isFormValid" variant="primary" size="small">
          {{ mode === 'edit' ? 'Bijwerken' : 'Toevoegen' }}
        </BaseButton>
        
        <BaseButton 
          v-if="mode === 'edit'"
          @click="$emit('cancel')"
          type="button"
          variant="secondary"
          size="small"
        >
          Annuleren
        </BaseButton>
      </div>
    </form>
  </div>
</template>

<script>
import { reactive, computed } from 'vue';
import BaseButton from '../ui/BaseButton.vue';

export default {
  name: 'DailyFoodEntryForm',
  components: { BaseButton },
  emits: ['submit', 'cancel'],
  props: {
    products: {
      type: Array,
      default: () => []
    },
    recipes: {
      type: Array,
      default: () => []
    },
    initialData: {
      type: Object,
      default: null
    },
    mode: {
      type: String,
      default: 'create',
      validator: value => ['create', 'edit'].includes(value)
    }
  },
  setup(props, { emit }) {
    const form = reactive({
      type: 'product',
      selectedId: null,
      amount: null,
      unit: 'gram'
    });

    // Initialize form with existing data for edit mode
    if (props.initialData) {
      form.type = props.initialData.product ? 'product' : 'recipe';
      form.selectedId = props.initialData.product_id || props.initialData.recipe_id;
      form.amount = props.initialData.amount;
      form.unit = props.initialData.unit;
    }

    // Set default unit when type changes initially
    if (form.type === 'recipe' && !props.initialData) {
      form.unit = 'portie';
      form.amount = 1;
    }

    const availableItems = computed(() => {
      return form.type === 'product' ? props.products : props.recipes;
    });

    const isFormValid = computed(() => {
      return form.selectedId && 
             form.amount > 0 && 
             form.unit.trim().length > 0;
    });

    const resetSelection = () => {
      form.selectedId = null;
      // Set default unit based on type
      if (form.type === 'recipe') {
        form.unit = 'portie';
        form.amount = 1;
      } else {
        form.unit = 'gram';
        form.amount = null;
      }
    };

    const handleSubmit = () => {
      if (isFormValid.value) {
        const submitData = {
          amount: form.amount,
          unit: form.unit
        };

        if (form.type === 'product') {
          submitData.product_id = form.selectedId;
          submitData.recipe_id = null;
        } else {
          submitData.recipe_id = form.selectedId;
          submitData.product_id = null;
        }

        emit('submit', submitData);
      }
    };

    return {
      form,
      availableItems,
      isFormValid,
      resetSelection,
      handleSubmit
    };
  }
}
</script>

<style scoped>
.entry-form {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.entry-form h4 {
  margin: 0 0 16px 0;
  color: #1f2937;
  font-size: 16px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>