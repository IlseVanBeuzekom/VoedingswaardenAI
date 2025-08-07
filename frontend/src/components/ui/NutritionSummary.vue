<template>
    <div class="nutrition-summary">
      <h4>Voedingswaarden per portie</h4>
      <div class="nutrition-grid">
        <div class="nutrition-item">
          <span class="nutrition-label">Energie</span>
          <span class="nutrition-value">{{ Math.round(nutritionData.energy_kcal) }} kcal</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrition-label">Eiwitten</span>
          <span class="nutrition-value">{{ formatValue(nutritionData.proteins) }}g</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrition-label">Koolhydraten</span>
          <span class="nutrition-value">{{ formatValue(nutritionData.carbohydrates) }}g</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrition-label">Waarvan suikers</span>
          <span class="nutrition-value">{{ formatValue(nutritionData.sugars) }}g</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrition-label">Vetten</span>
          <span class="nutrition-value">{{ formatValue(nutritionData.fats) }}g</span>
        </div>
        <div class="nutrition-item">
          <span class="nutrition-label">Vezels</span>
          <span class="nutrition-value">{{ formatValue(nutritionData.fibers) }}g</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NutritionSummary',
    props: {
      nutritionData: {
        type: Object,
        required: true
      }
    },
    setup() {
      const formatValue = (value) => {
        return Math.round(value * 10) / 10;
      };
  
      return {
        formatValue
      };
    }
  }
  </script>
  
  <style scoped>
  .nutrition-summary {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
  }
  
  .nutrition-summary h4 {
    margin: 0 0 16px 0;
    color: #1f2937;
    font-size: 16px;
    font-weight: 600;
  }
  
  .nutrition-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
  }
  
  .nutrition-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: white;
    border-radius: 6px;
    border: 1px solid #e5e7eb;
  }
  
  .nutrition-label {
    font-size: 14px;
    color: #374151;
    font-weight: 500;
  }
  
  .nutrition-value {
    font-size: 14px;
    color: #1f2937;
    font-weight: 600;
  }
  
  @media (max-width: 768px) {
    .nutrition-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>