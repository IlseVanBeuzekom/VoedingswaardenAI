<template>
    <div class="chart-wrapper">
      <div v-if="hasData" class="pie-chart-container">
        <svg :width="size" :height="size" class="pie-chart">
          <g :transform="`translate(${center}, ${center})`">
            <path
              v-for="(segment, index) in segments"
              :key="index"
              :d="segment.path"
              :fill="segment.color"
              class="segment"
            />
          </g>
        </svg>
        
        <div class="legend">
          <div 
            v-for="(item, index) in legendItems" 
            :key="index" 
            class="legend-item"
          >
            <div 
              class="legend-color" 
              :style="{ backgroundColor: item.color }"
            ></div>
            <span class="legend-label">{{ item.label }}</span>
            <span class="legend-value">{{ item.value }}g ({{ item.percentage }}%)</span>
          </div>
        </div>
      </div>
      
      <div v-else class="no-data">
        Geen data beschikbaar
      </div>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  
  export default {
    name: 'MacronutrientChart',
    props: {
      nutrition: {
        type: Object,
        required: true
      },
      size: {
        type: Number,
        default: 200
      }
    },
    setup(props) {
      const center = computed(() => props.size / 2);
      const radius = computed(() => props.size / 2 - 20);
  
      const colors = {
        proteins: '#dc2626',
        carbohydrates: '#d97706', 
        fats: '#16a34a'
      };
  
      const hasData = computed(() => {
        const total = props.nutrition.proteins + props.nutrition.carbohydrates + props.nutrition.fats;
        return total > 0;
      });
  
      const total = computed(() => {
        return props.nutrition.proteins + props.nutrition.carbohydrates + props.nutrition.fats;
      });
  
      const segments = computed(() => {
        if (!hasData.value) return [];
  
        const data = [
          { label: 'Eiwitten', value: props.nutrition.proteins, color: colors.proteins },
          { label: 'Koolhydraten', value: props.nutrition.carbohydrates, color: colors.carbohydrates },
          { label: 'Vetten', value: props.nutrition.fats, color: colors.fats }
        ];
  
        let currentAngle = 0;
        
        return data.map(item => {
          const percentage = (item.value / total.value) * 100;
          const angle = (item.value / total.value) * 2 * Math.PI;
          
          const x1 = Math.cos(currentAngle) * radius.value;
          const y1 = Math.sin(currentAngle) * radius.value;
          
          currentAngle += angle;
          
          const x2 = Math.cos(currentAngle) * radius.value;
          const y2 = Math.sin(currentAngle) * radius.value;
          
          const largeArcFlag = angle > Math.PI ? 1 : 0;
          
          const pathData = [
            'M', 0, 0,
            'L', x1, y1,
            'A', radius.value, radius.value, 0, largeArcFlag, 1, x2, y2,
            'Z'
          ].join(' ');
  
          return {
            path: pathData,
            color: item.color,
            percentage: Math.round(percentage)
          };
        });
      });
  
      const legendItems = computed(() => {
        if (!hasData.value) return [];
  
        return [
          {
            label: 'Eiwitten',
            value: Math.round(props.nutrition.proteins * 10) / 10,
            percentage: Math.round((props.nutrition.proteins / total.value) * 100),
            color: colors.proteins
          },
          {
            label: 'Koolhydraten',
            value: Math.round(props.nutrition.carbohydrates * 10) / 10,
            percentage: Math.round((props.nutrition.carbohydrates / total.value) * 100),
            color: colors.carbohydrates
          },
          {
            label: 'Vetten',
            value: Math.round(props.nutrition.fats * 10) / 10,
            percentage: Math.round((props.nutrition.fats / total.value) * 100),
            color: colors.fats
          }
        ];
      });
  
      return {
        center,
        hasData,
        segments,
        legendItems
      };
    }
  }
  </script>
  
  <style scoped>
  .chart-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  
  .pie-chart-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
  
  .pie-chart {
    drop-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .segment {
    transition: opacity 0.2s ease;
    cursor: pointer;
  }
  
  .segment:hover {
    opacity: 0.8;
  }
  
  .legend {
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 200px;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
  }
  
  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    flex-shrink: 0;
  }
  
  .legend-label {
    flex: 1;
    color: #374151;
    font-weight: 500;
  }
  
  .legend-value {
    color: #6b7280;
    font-weight: 600;
  }
  
  .no-data {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #6b7280;
    font-style: italic;
  }
  
  @media (max-width: 768px) {
    .pie-chart-container {
      scale: 0.8;
    }
  }
  </style>