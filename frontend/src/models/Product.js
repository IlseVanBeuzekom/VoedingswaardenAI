export class Product {
    constructor(data = {}) {
      this.id = data.id || null;
      this.name = data.name || '';
      this.serving_size = data.serving_size || 100.0;  // NIEUW: default 100g
      this.energy_kcal = data.energy_kcal || 0;
      this.fats = data.fats || 0;
      this.carbohydrates = data.carbohydrates || 0;
      this.sugars = data.sugars || 0;
      this.fibers = data.fibers || 0;
      this.proteins = data.proteins || 0;
    }
  
    static fromAPI(apiData) {
      return new Product(apiData);
    }
  
    toAPI() {
      return {
        name: this.name,
        serving_size: this.serving_size,  // NIEUW
        energy_kcal: this.energy_kcal,
        fats: this.fats,
        carbohydrates: this.carbohydrates,
        sugars: this.sugars,
        fibers: this.fibers,
        proteins: this.proteins
      };
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
  }