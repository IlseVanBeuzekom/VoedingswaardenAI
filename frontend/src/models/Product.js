export class Product {
  constructor(data = {}) {
    this.id = data.id || null;
    this.name = data.name || '';
    this.serving_size = data.serving_size || 100.0;  // Still in grams for backend
    this.serving_unit = data.serving_unit || 'gram'; // Display unit
    this.serving_amount = data.serving_amount || 100; // Display amount
    this.energy_kcal = data.energy_kcal || 0;
    this.fats = data.fats || 0;
    this.carbohydrates = data.carbohydrates || 0;
    this.sugars = data.sugars || 0;
    this.fibers = data.fibers || 0;
    this.proteins = data.proteins || 0;
  }

  static fromAPI(apiData) {
    const product = new Product(apiData);
    
    // If we have serving_unit info, use it, otherwise default to gram
    if (!apiData.serving_unit) {
      product.serving_unit = 'gram';
      product.serving_amount = apiData.serving_size || 100;
    }
    
    return product;
  }

  toAPI() {
    return {
      name: this.name,
      serving_size: this.serving_size, // Backend expects grams
      energy_kcal: this.energy_kcal,
      fats: this.fats,
      carbohydrates: this.carbohydrates,
      sugars: this.sugars,
      fibers: this.fibers,
      proteins: this.proteins
    };
  }

  // Helper method to get unit display text
  getUnitDisplay() {
    const unitMap = {
      'gram': 'gram',
      'stuk': 'stuk',
      'ml': 'ml',
      'kopje': 'kopje',
      'el': 'eetlepel',
      'tl': 'theelepel'
    };
    return unitMap[this.serving_unit] || this.serving_unit;
  }

  // Get display text for serving size
  getServingDisplay() {
    return `${this.serving_amount} ${this.getUnitDisplay()}`;
  }

  getPer100g() {
    const factor = 100 / this.serving_size;
    return {
      energy_kcal: (this.energy_kcal * factor).toFixed(1),
      fats: (this.fats * factor).toFixed(1),
      carbohydrates: (this.carbohydrates * factor).toFixed(1),
      sugars: (this.sugars * factor).toFixed(1),
      fibers: (this.fibers * factor).toFixed(1),
      proteins: (this.proteins * factor).toFixed(1)
    };
  }

  getForAmount(grams) {
    const factor = grams / this.serving_size;
    return {
      energy_kcal: (this.energy_kcal * factor).toFixed(1),
      fats: (this.fats * factor).toFixed(1),
      carbohydrates: (this.carbohydrates * factor).toFixed(1),
      sugars: (this.sugars * factor).toFixed(1),
      fibers: (this.fibers * factor).toFixed(1),
      proteins: (this.proteins * factor).toFixed(1)
    };
  }

  // Get nutrition for a specific serving amount in the product's unit
  getForServings(servingCount) {
    const factor = servingCount;
    return {
      energy_kcal: (this.energy_kcal * factor).toFixed(1),
      fats: (this.fats * factor).toFixed(1),
      carbohydrates: (this.carbohydrates * factor).toFixed(1),
      sugars: (this.sugars * factor).toFixed(1),
      fibers: (this.fibers * factor).toFixed(1),
      proteins: (this.proteins * factor).toFixed(1)
    };
  }
}