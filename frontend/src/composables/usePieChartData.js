// frontend/src/composables/usePieChartData.js
export const usePieChartData = () => {
  const mealConfig = {
    ontbijt: { displayName: 'Ontbijt', color: '#f59e0b' },
    lunch: { displayName: 'Lunch', color: '#10b981' },
    diner: { displayName: 'Diner', color: '#3b82f6' },
    tussendoortje: { displayName: 'Tussendoortje', color: '#8b5cf6' }
  };

  const macronutrientColors = {
    proteins: '#dc2626',
    carbohydrates: '#d97706', 
    fats: '#16a34a'
  };

  const getMacronutrientData = (nutrition) => {
    return [
      { 
        label: 'Eiwitten', 
        value: nutrition.proteins, 
        color: macronutrientColors.proteins 
      },
      { 
        label: 'Koolhydraten', 
        value: nutrition.carbohydrates, 
        color: macronutrientColors.carbohydrates 
      },
      { 
        label: 'Vetten', 
        value: nutrition.fats, 
        color: macronutrientColors.fats 
      }
    ];
  };

  const getMealCaloriesData = (entries) => {
    const mealTotals = {};
    
    entries.forEach(entry => {
      const mealType = entry.meal_type || 'tussendoortje';
      const nutrition = entry.calculateNutrition();
      
      if (!mealTotals[mealType]) {
        mealTotals[mealType] = 0;
      }
      
      mealTotals[mealType] += nutrition.energy_kcal;
    });

    return Object.entries(mealTotals)
      .filter(([_, calories]) => calories > 0)
      .map(([type, calories]) => ({
        label: mealConfig[type]?.displayName || type,
        value: Math.round(calories),
        color: mealConfig[type]?.color || '#6b7280'
      }));
  };

  const getMealCarbsData = (entries) => {
    const mealTotals = {};
    
    entries.forEach(entry => {
      const mealType = entry.meal_type || 'tussendoortje';
      const nutrition = entry.calculateNutrition();
      
      if (!mealTotals[mealType]) {
        mealTotals[mealType] = 0;
      }
      
      mealTotals[mealType] += nutrition.carbohydrates;
    });

    return Object.entries(mealTotals)
      .filter(([_, carbs]) => carbs > 0)
      .map(([type, carbs]) => ({
        label: mealConfig[type]?.displayName || type,
        value: Math.round(carbs * 10) / 10,
        color: mealConfig[type]?.color || '#6b7280'
      }));
  };

  return {
    getMacronutrientData,
    getMealCaloriesData,
    getMealCarbsData
  };
};