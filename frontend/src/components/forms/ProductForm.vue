<template>
    <form @submit.prevent="handleSubmit" class="product-form">
      <h2>{{ mode === 'edit' ? 'Product Bewerken' : 'Nieuw Product Toevoegen' }}</h2>
      
      <div class="form-group">
        <label for="name">Productnaam*</label>
        <input
          v-model="form.name"
          type="text"
          id="name"
          required
          class="form-input"
          placeholder="Bijv. Volkoren brood"
        />
      </div>

      <div class="form-group">
        <label for="serving_size">Portiegrootte (gram)*</label>
        <input
          v-model.number="form.serving_size"
          type="number"
          id="serving_size"
          step="0.1"
          min="0.1"
          required
          class="form-input"
          placeholder="100"
        />
        <small class="form-help">
          De voedingswaarden worden berekend per {{ form.serving_size }}g
        </small>
      </div>

  
      <div class="nutrition-grid">
        <div class="form-group">
          <label for="energy">Energie (kcal)*</label>
          <input
            v-model.number="form.energy_kcal"
            type="number"
            id="energy"
            step="0.1"
            min="0"
            required
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label for="fats">Vetten (g)*</label>
          <input
            v-model.number="form.fats"
            type="number"
            id="fats"
            step="0.1"
            min="0"
            required
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label for="carbs">Koolhydraten (g)*</label>
          <input
            v-model.number="form.carbohydrates"
            type="number"
            id="carbs"
            step="0.1"
            min="0"
            required
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label for="sugars">Waarvan suikers (g)*</label>
          <input
            v-model.number="form.sugars"
            type="number"
            id="sugars"
            step="0.1"
            min="0"
            required
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label for="fibers">Vezels (g)*</label>
          <input
            v-model.number="form.fibers"
            type="number"
            id="fibers"
            step="0.1"
            min="0"
            required
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label for="proteins">Eiwitten (g)*</label>
          <input
            v-model.number="form.proteins"
            type="number"
            id="proteins"
            step="0.1"
            min="0"
            required
            class="form-input"
          />
        </div>
      </div>
  
      <div class="form-actions">
        <BaseButton 
          type="submit"
          :disabled="!isFormValid || loading"
          variant="primary"
        >
        {{ loading ? 'Bezig met opslaan...' : (mode === 'edit' ? 'Product Bijwerken' : 'Product Toevoegen') }}
        </BaseButton>
        
        <BaseButton 
          @click="$emit('cancel')"
          variant="secondary"
          type="button"
        >
          Annuleren
        </BaseButton>
      </div>
  
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </form>
  </template>
  
  <script>
  import { reactive, computed, watch } from 'vue';
  import BaseButton from '../ui/BaseButton.vue';
  import { Product } from '../../models/Product.js';
  
  export default {
    name: 'ProductForm',
    components: {
      BaseButton
    },
    emits: ['submit', 'cancel'],
    props: {
      loading: {
        type: Boolean,
        default: false
      },
      error: {
        type: String,
        default: null
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
      const form = reactive(new Product());
  
      watch(() => props.initialData, (newData) => {
        if (newData) {
          Object.assign(form, newData)
        }
      }, {immediate: true });
      
      const isFormValid = computed(() => {
        return form.name.trim().length > 0 &&
               form.serving_size > 0 &&
               form.energy_kcal >= 0 &&
               form.fats >= 0 &&
               form.carbohydrates >= 0 &&
               form.sugars >= 0 &&
               form.fibers >= 0 &&
               form.proteins >= 0;
      });
  
      const handleSubmit = () => {
        if (isFormValid.value) {
          emit('submit', form.toAPI());
        }
      };
  
      return {
        form,
        isFormValid,
        handleSubmit
      };
    }
  }
  </script>
  
  <style scoped>
  .form-help {
    display: block;
    margin-top: 4px;
    font-size: 14px;
    color: #6b7280;
    font-style: italic;
  }

  .product-form {
    max-width: 600px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .product-form h2 {
    margin-bottom: 24px;
    color: #1f2937;
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 6px;
    font-weight: 500;
    color: #374151;
  }
  
  .form-input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.2s ease;
  }
  
  .form-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .nutrition-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }
  
  .form-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 24px;
  }
  
  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 12px;
    border-radius: 6px;
    margin-top: 16px;
    text-align: center;
  }
  
  @media (max-width: 768px) {
    .nutrition-grid {
      grid-template-columns: 1fr;
    }
    
    .form-actions {
      flex-direction: column;
    }
  }
  </style>
  