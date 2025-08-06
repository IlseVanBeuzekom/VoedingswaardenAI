<template>
    <div class="date-range-selector">
      <h3>{{ title }}</h3>
      <div class="date-inputs">
        <div class="input-group">
          <label for="start-date">Van:</label>
          <input
            id="start-date"
            v-model="startDate"
            type="date"
            class="date-input"
            @change="onDateChange"
          />
        </div>
        
        <div class="input-group">
          <label for="end-date">Tot:</label>
          <input
            id="end-date"
            v-model="endDate"
            type="date"
            class="date-input"
            @change="onDateChange"
          />
        </div>
        
        <BaseButton 
          v-if="showQuickWeek"
          @click="setCurrentWeek"
          variant="secondary"
          size="small"
        >
          Deze week
        </BaseButton>
      </div>
      
      <div v-if="isValidRange && dayCount > 0" class="range-info">
        {{ dayCount }} dagen geselecteerd ({{ formatDate(startDate) }} - {{ formatDate(endDate) }})
      </div>
      
      <div v-else-if="startDate && endDate && !isValidRange" class="error-info">
        Einddatum moet na startdatum liggen
      </div>
    </div>
  </template>
  
  <script>
  import { computed, ref, watch } from 'vue';
  import BaseButton from './BaseButton.vue';
  
  export default {
    name: 'DateRangeSelector',
    components: { BaseButton },
    emits: ['dateChange'],
    props: {
      title: {
        type: String,
        default: 'Selecteer periode'
      },
      initialStartDate: {
        type: String,
        default: null
      },
      initialEndDate: {
        type: String,
        default: null
      },
      showQuickWeek: {
        type: Boolean,
        default: true
      }
    },
    setup(props, { emit }) {
      const startDate = ref(props.initialStartDate || '');
      const endDate = ref(props.initialEndDate || '');
  
      const isValidRange = computed(() => {
        if (!startDate.value || !endDate.value) return false;
        return new Date(startDate.value) <= new Date(endDate.value);
      });
  
      const dayCount = computed(() => {
        if (!isValidRange.value) return 0;
        const start = new Date(startDate.value);
        const end = new Date(endDate.value);
        const diffTime = Math.abs(end - start);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
      });
  
      const setCurrentWeek = () => {
        const today = new Date();
        const monday = new Date(today);
        const dayOfWeek = today.getDay();
        const diff = dayOfWeek === 0 ? -6 : 1 - dayOfWeek; // Adjust for Sunday
        monday.setDate(today.getDate() + diff);
  
        const sunday = new Date(monday);
        sunday.setDate(monday.getDate() + 6);
  
        startDate.value = formatDateForInput(monday);
        endDate.value = formatDateForInput(sunday);
        onDateChange();
      };
  
      const formatDateForInput = (date) => {
        return date.toISOString().split('T')[0];
      };
  
      const formatDate = (dateStr) => {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return date.toLocaleDateString('nl-NL', { 
          weekday: 'short', 
          day: 'numeric', 
          month: 'short' 
        });
      };
  
      const onDateChange = () => {
        if (isValidRange.value) {
          emit('dateChange', {
            startDate: startDate.value,
            endDate: endDate.value,
            dayCount: dayCount.value
          });
        }
      };
  
      // Watch for prop changes
      watch(() => props.initialStartDate, (newVal) => {
        if (newVal) startDate.value = newVal;
      });
  
      watch(() => props.initialEndDate, (newVal) => {
        if (newVal) endDate.value = newVal;
      });
  
      return {
        startDate,
        endDate,
        isValidRange,
        dayCount,
        setCurrentWeek,
        formatDate,
        onDateChange
      };
    }
  }
  </script>
  
  <style scoped>
  .date-range-selector {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
  }
  
  .date-range-selector h3 {
    margin: 0 0 16px 0;
    color: #1f2937;
  }
  
  .date-inputs {
    display: flex;
    gap: 16px;
    align-items: end;
    flex-wrap: wrap;
  }
  
  .input-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .input-group label {
    font-size: 14px;
    font-weight: 500;
    color: #374151;
  }
  
  .date-input {
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
  }
  
  .date-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .range-info {
    margin-top: 12px;
    padding: 8px 12px;
    background-color: #f0f9ff;
    color: #0369a1;
    border-radius: 6px;
    font-size: 14px;
  }
  
  .error-info {
    margin-top: 12px;
    padding: 8px 12px;
    background-color: #fef2f2;
    color: #dc2626;
    border-radius: 6px;
    font-size: 14px;
  }
  
  @media (max-width: 768px) {
    .date-inputs {
      flex-direction: column;
      align-items: stretch;
    }
  }
  </style>