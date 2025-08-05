<template>
    <div class="recipe-card">
      <div class="card-actions">
        <button 
          @click="$emit('edit', recipe.id)"
          class="action-btn edit-btn"
          title="Recept bewerken"
        >
          ✏️
        </button>
        <button 
          @click="$emit('delete', recipe.id)"
          class="action-btn delete-btn"
          title="Recept verwijderen"
        >
          ❌
        </button>
      </div>
  
      <h3>{{ recipe.name }}</h3>
      
      <div class="recipe-meta">
        <div class="meta-item">
          <span class="meta-label">👥</span>
          <span>{{ recipe.servings }} personen</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">⏱️</span>
          <span>{{ recipe.preparation_time }} min</span>
        </div>
      </div>
  
      <div class="ingredients-preview">
        <h4>Ingrediënten ({{ recipe.ingredients.length }})</h4>
        <div class="ingredients-list">
          <div 
            v-for="ingredient in recipe.ingredients.slice(0, 3)" 
            :key="ingredient.id"
            class="ingredient-item"
          >
            {{ ingredient.amount }} {{ ingredient.unit }} {{ ingredient.product?.name }}
          </div>
          <div v-if="recipe.ingredients.length > 3" class="more-ingredients">
            +{{ recipe.ingredients.length - 3 }} meer...
          </div>
        </div>
      </div>
  
      <div class="instructions-preview">
        <h4>Bereiding</h4>
        <p>{{ truncatedInstructions }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  
  export default {
    name: 'RecipeCard',
    emits: ['edit', 'delete'],
    props: {
      recipe: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const truncatedInstructions = computed(() => {
        const maxLength = 120;
        if (props.recipe.instructions.length <= maxLength) {
          return props.recipe.instructions;
        }
        return props.recipe.instructions.substring(0, maxLength) + '...';
      });
  
      return {
        truncatedInstructions
      };
    }
  }
  </script>
  
  <style scoped>
  .recipe-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    transition: box-shadow 0.2s ease;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .recipe-card:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  
  .card-actions {
    position: absolute;
    top: 12px;
    right: 12px;
    display: flex;
    gap: 8px;
  }
  
  .action-btn {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
  }
  
  .action-btn:hover {
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
  }
  
  .edit-btn:hover {
    border-color: #3b82f6;
  }
  
  .delete-btn:hover {
    border-color: #ef4444;
  }
  
  .recipe-card h3 {
    margin: 0;
    color: #1f2937;
    font-size: 1.25rem;
    padding-right: 80px;
  }
  
  .recipe-meta {
    display: flex;
    gap: 16px;
  }
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #6b7280;
    font-size: 14px;
  }
  
  .meta-label {
    font-size: 16px;
  }
  
  .ingredients-preview h4,
  .instructions-preview h4 {
    margin: 0 0 8px 0;
    color: #374151;
    font-size: 14px;
    font-weight: 600;
  }
  
  .ingredients-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .ingredient-item {
    font-size: 13px;
    color: #6b7280;
    line-height: 1.4;
  }
  
  .more-ingredients {
    font-size: 13px;
    color: #9ca3af;
    font-style: italic;
  }
  
  .instructions-preview p {
    margin: 0;
    font-size: 13px;
    color: #6b7280;
    line-height: 1.4;
  }
  </style>