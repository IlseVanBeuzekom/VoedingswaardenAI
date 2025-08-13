export class Recipe {
    constructor(data = {}) {
      this.id = data.id || null;
      this.name = data.name || '';
      this.servings = data.servings || 4;
      this.preparation_time = data.preparation_time || 30;
      this.instructions = data.instructions || '';
      this.image_url = data.image_url || null;
      this.ingredients = data.ingredients ? data.ingredients.map(ing => new RecipeIngredient(ing)) : [];
    }
  
    static fromAPI(apiData) {
      return new Recipe(apiData);
    }
  
    toAPI() {
      return {
        name: this.name,
        servings: this.servings,
        preparation_time: this.preparation_time,
        instructions: this.instructions,
        image_url: this.image_url,
        ingredients: this.ingredients.map(ing => ing.toAPI())
      };
    }
  
    addIngredient(ingredient = {}) {
      this.ingredients.push(new RecipeIngredient(ingredient));
    }
  
    removeIngredient(index) {
      this.ingredients.splice(index, 1);
    }
  }
  
  export class RecipeIngredient {
    constructor(data = {}) {
      this.id = data.id || null;
      this.product_id = data.product_id || null;
      this.amount = data.amount || 0;
      this.unit = data.unit || 'gram';
      this.product = data.product || null;
    }
  
    static fromAPI(apiData) {
      return new RecipeIngredient(apiData);
    }
  
    toAPI() {
      return {
        product_id: this.product_id,
        amount: this.amount,
        unit: this.unit
      };
    }
  }