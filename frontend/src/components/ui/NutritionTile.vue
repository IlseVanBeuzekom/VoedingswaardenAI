<template>
    <div class="nutrition-tile" :class="`tile-${color}`">
      <div class="tile-icon">
        {{ getIcon() }}
      </div>
      <div class="tile-content">
        <h4>{{ title }}</h4>
        <div class="tile-value">
          {{ value }} <span class="unit">{{ unit }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NutritionTile',
    props: {
      title: {
        type: String,
        required: true
      },
      value: {
        type: [Number, String],
        required: true
      },
      unit: {
        type: String,
        required: true
      },
      color: {
        type: String,
        default: 'blue',
        validator: value => ['blue', 'red', 'green', 'yellow'].includes(value)
      }
    },
    setup(props) {
      const getIcon = () => {
        const icons = {
          'Energie': '🔥',
          'Eiwitten': '🥩',
          'Koolhydraten': '🌾', 
          'Vetten': '🥑'
        };
        return icons[props.title] || '📊';
      };
  
      return {
        getIcon
      };
    }
  }
  </script>
  
  <style scoped>
  .nutrition-tile {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e5e7eb;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: transform 0.2s ease;
  }
  
  .nutrition-tile:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .tile-icon {
    font-size: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    border-radius: 50%;
  }
  
  .tile-blue .tile-icon {
    background: #dbeafe;
  }
  
  .tile-red .tile-icon {
    background: #fecaca;
  }
  
  .tile-green .tile-icon {
    background: #dcfce7;
  }
  
  .tile-yellow .tile-icon {
    background: #fef3c7;
  }
  
  .tile-content {
    flex: 1;
  }
  
  .tile-content h4 {
    margin: 0 0 8px 0;
    font-size: 16px;
    font-weight: 600;
    color: #374151;
  }
  
  .tile-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
  }
  
  .tile-blue .tile-value {
    color: #2563eb;
  }
  
  .tile-red .tile-value {
    color: #dc2626;
  }
  
  .tile-green .tile-value {
    color: #16a34a;
  }
  
  .tile-yellow .tile-value {
    color: #d97706;
  }
  
  .unit {
    font-size: 1rem;
    font-weight: 500;
    opacity: 0.8;
  }
  
  @media (max-width: 768px) {
    .nutrition-tile {
      padding: 20px;
    }
    
    .tile-icon {
      font-size: 2rem;
      width: 56px;
      height: 56px;
    }
    
    .tile-value {
      font-size: 1.5rem;
    }
  }
  </style>