export class WeekMenu {
    constructor(data = {}) {
      this.id = data.id || null;
      this.start_date = data.start_date || '';
      this.end_date = data.end_date || '';
      this.days = data.days ? data.days.map(day => new MenuDay(day)) : [];
    }
  
    static fromAPI(apiData) {
      return new WeekMenu(apiData);
    }
  
    toAPI() {
      return {
        start_date: this.start_date,
        end_date: this.end_date,
        days: this.days.map(day => day.toAPI())
      };
    }
  
    addDay(dayData = {}) {
      this.days.push(new MenuDay(dayData));
    }
  
    removeDay(index) {
      this.days.splice(index, 1);
    }
  
    getDayByDate(dateStr) {
      return this.days.find(day => day.date === dateStr);
    }
  }
  
  export class MenuDay {
    constructor(data = {}) {
      this.id = data.id || null;
      this.date = data.date || '';
      this.recipe_id = data.recipe_id || null;
      this.recipe = data.recipe || null;
      this.servings = data.servings || null;
      this.add_to_shopping_list = data.add_to_shopping_list !== undefined ? data.add_to_shopping_list : true;
    }
  
    static fromAPI(apiData) {
      return new MenuDay(apiData);
    }
  
    toAPI() {
      return {
        date: this.date,
        recipe_id: this.recipe_id,
        servings: this.servings,
        add_to_shopping_list: this.add_to_shopping_list
      };
    }
  }