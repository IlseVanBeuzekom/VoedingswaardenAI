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

    <div class="serving-section">
      <h3>Portiegrootte</h3>
      <div class="serving-controls">
        <div class="form-group">
          <label for="serving_size">Hoeveelheid*</label>
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
        </div>
        
        <div class="form-group">
          <label for="serving_unit">Eenheid*</label>
          <select 
            v-model="form.serving_unit" 
            id="serving_unit"
            class="form-input"
            @change="onServingUnitChange"
          >
            <option value="gram">gram</option>
            <option value="stuk">stuk</option>
            <option value="ml">ml</option>
            <option value="kopje">kopje (250ml)</option>
            <option value="el">eetlepel (15ml)</option>
            <option value="tl">theelepel (5ml)</option>
          </select>
        </div>
      </div>
      
      <small class="form-help">
        De voedingswaarden hieronder zijn per {{ form.serving_size }} {{ getUnitDisplay(form.serving_unit) }}
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

    <!-- Per 100g preview for non-gram units -->
    <div v-if="form.serving_unit !== 'gram' && isFormValid" class="per-100g-preview">
      <h4>Omgerekend per 100g:</h4>
      <div class="nutrition-compact">
        <span>{{ calculatePer100g().energy_kcal }} kcal</span>
        <span>{{ calculatePer100g().fats }}g vet</span>
        <span>{{ calculatePer100g().carbohydrates }}g kh</span>
        <span>{{ calculatePer100g().proteins }}g eiw</span>
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
    // Add serving_unit to form
    form.serving_unit = 'gram';

    watch(() => props.initialData, (newData) => {
      if (newData) {
        Object.assign(form, newData);
        // Set serving_unit based on existing data or default to gram
        form.serving_unit = newData.serving_unit || 'gram';
      }
    }, {immediate: true });

    const getUnitDisplay = (unit) => {
      const unitMap = {
        'gram': 'gram',
        'stuk': 'stuk',
        'ml': 'ml',
        'kopje': 'kopje',
        'el': 'eetlepel',
        'tl': 'theelepel'
      };
      return unitMap[unit] || unit;
    };

    const getGramEquivalent = (amount, unit) => {
      // Convert different units to grams for calculation
      const conversions = {
        'gram': 1,
        'stuk': 1, // Will be handled as-is in serving_size
        'ml': 1, // Assume 1ml = 1g for liquids
        'kopje': 250, // 250ml/g
        'el': 15, // 15ml/g  
        'tl': 5 // 5ml/g
      };
      
      if (unit === 'stuk') {
        // For pieces, we can't convert to grams directly
        // Return the serving_size as-is
        return amount;
      }
      
      return amount * (conversions[unit] || 1);
    };

    const calculatePer100g = () => {
      if (!form.serving_unit || form.serving_unit === 'stuk') {
        return {
          energy_kcal: '?',
          fats: '?',
          carbohydrates: '?',
          proteins: '?'
        };
      }

      const gramEquivalent = getGramEquivalent(form.serving_size, form.serving_unit);
      const factor = 100 / gramEquivalent;
      
      return {
        energy_kcal: Math.round(form.energy_kcal * factor * 10) / 10,
        fats: Math.round(form.fats * factor * 10) / 10,
        carbohydrates: Math.round(form.carbohydrates * factor * 10) / 10,
        proteins: Math.round(form.proteins * factor * 10) / 10
      };
    };
    
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

    const onServingUnitChange = () => {
      // Reset serving size to sensible defaults when unit changes
      const defaultSizes = {
        'gram': 100,
        'stuk': 1,
        'ml': 100,
        'kopje': 1,
        'el': 1,
        'tl': 1
      };
      form.serving_size = defaultSizes[form.serving_unit] || 100;
    };

    const handleSubmit = () => {
      if (isFormValid.value) {
        const submitData = form.toAPI();
        // Store the gram equivalent in serving_size for backend
        submitData.serving_size = getGramEquivalent(form.serving_size, form.serving_unit);
        // Store unit info for frontend use
        submitData.serving_unit = form.serving_unit;
        submitData.serving_amount = form.serving_size;
        
        emit('submit', submitData);
      }
    };

    return {
      form,
      isFormValid,
      handleSubmit,
      getUnitDisplay,
      calculatePer100g,
      onServingUnitChange
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

.serving-section {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.serving-section h3 {
  margin: 0 0 16px 0;
  color: #374151;
  font-size: 16px;
  font-weight: 600;
}

.serving-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
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

.per-100g-preview {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.per-100g-preview h4 {
  margin: 0 0 8px 0;
  color: #0369a1;
  font-size: 14px;
}

.nutrition-compact {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 14px;
  color: #0369a1;
}

.nutrition-compact span {
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #bae6fd;
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

  .serving-controls {
    grid-template-columns: 1fr;
  }

  .nutrition-compact {
    flex-direction: column;
    gap: 8px;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>