export class DailyFoodLog {
    constructor(data = {}) {
      this.id = data.id || null;
      this.date = data.date || null;
      this.entries = data.entries ? data.entries.map(entry => new DailyFoodEntry(entry)) : [];
    }
  
    static fromAPI(apiData) {
      return new DailyFoodLog(apiData);
    }
  
    calculateTotalNutrition() {
      if (this.entries.length === 0) {
        return {
          energy_kcal: 0,
          proteins: 0,
          carbohydrates: 0,
          sugars: 0,
          fats: 0,
          fibers: 0
        };
      }
  
      return this.entries.reduce((totals, entry) => {
        const nutrition = entry.calculateNutrition();
        totals.energy_kcal += nutrition.energy_kcal;
        totals.proteins += nutrition.proteins;
        totals.carbohydrates += nutrition.carbohydrates;
        totals.sugars += nutrition.sugars;
        totals.fats += nutrition.fats;
        totals.fibers += nutrition.fibers;
        return totals;
      }, {
        energy_kcal: 0,
        proteins: 0,
        carbohydrates: 0,
        sugars: 0,
        fats: 0,
        fibers: 0
      });
    }
  }
  
  export class DailyFoodEntry {
    constructor(data = {}) {
      this.id = data.id || null;
      this.product_id = data.product_id || null;
      this.recipe_id = data.recipe_id || null;
      this.amount = data.amount || 0;
      this.unit = data.unit || 'gram';
      this.product = data.product || null;
      this.recipe = data.recipe || null;
    }
  
    static fromAPI(apiData) {
      return new DailyFoodEntry(apiData);
    }
  
    toAPI() {
      return {
        product_id: this.product_id,
        recipe_id: this.recipe_id,
        amount: this.amount,
        unit: this.unit
      };
    }
  
    getName() {
      if (this.product) return this.product.name;
      if (this.recipe) return this.recipe.name;
      return 'Unknown';
    }
  
    getType() {
      return this.product ? 'product' : 'recipe';
    }
  
    calculateNutrition() {
      if (this.product) {
        return this.calculateProductNutrition();
      } else if (this.recipe) {
        return this.calculateRecipeNutrition();
      }
      
      return {
        energy_kcal: 0,
        proteins: 0,
        carbohydrates: 0,
        sugars: 0,
        fats: 0,
        fibers: 0
      };
    }
  
    calculateProductNutrition() {
      const factor = this.amount / this.product.serving_size;
      
      return {
        energy_kcal: (this.product.energy_kcal || 0) * factor,
        proteins: (this.product.proteins || 0) * factor,
        carbohydrates: (this.product.carbohydrates || 0) * factor,
        sugars: (this.product.sugars || 0) * factor,
        fats: (this.product.fats || 0) * factor,
        fibers: (this.product.fibers || 0) * factor
      };
    }
  
    calculateRecipeNutrition() {
      // For recipes, we assume the nutrition values are per serving
      // and we calculate based on servings consumed
      const servingsConsumed = this.amount / this.recipe.servings;
      
      // Note: Recipe nutrition calculation would need recipe ingredients data
      // This is simplified - in practice you'd calculate from recipe ingredients
      return {
        energy_kcal: 0, // Would calculate from recipe ingredients
        proteins: 0,
        carbohydrates: 0,
        sugars: 0,
        fats: 0,
        fibers: 0
      };
    }
  }