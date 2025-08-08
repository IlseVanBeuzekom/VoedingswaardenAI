<template>
  <div class="home">
    <div class="hero">
      <h1>Voedingswaarden App</h1>
      <p>Beheer je producten, recepten en dagelijkse voeding</p>
    </div>

    <div class="actions">
      <div class="action-groups">
      <div class="action-group">
        <h2>Producten</h2>
        <div class="group-buttons">
          <BaseButton 
            @click="$router.push('/products/add')"
            variant="primary"
            size="large"
          >
            Voeg Product Toe
          </BaseButton>
          
          <BaseButton 
            @click="$router.push('/products')"
            variant="secondary"
            size="large"
          >
            Product Overzicht
          </BaseButton>
        </div>
      </div>

      <div class="action-group">
        <h2>Recepten</h2>
        <div class="group-buttons">
          <BaseButton 
            @click="$router.push('/recipes/add')"
            variant="primary"
            size="large"
          >
            Voeg Recept Toe
          </BaseButton>
          
          <BaseButton 
            @click="$router.push('/recipes')"
            variant="secondary"
            size="large"
          >
            Recept Overzicht
          </BaseButton>
        </div>
      </div>

      <div class="action-group">
        <h2>Weekmenu</h2>
        <div class="group-buttons">
          <BaseButton 
            @click="$router.push('/weekmenu')"
            variant="primary"
            size="large"
          >
            Plan Weekmenu
          </BaseButton>
        </div>
      </div>

      <div class="action-group">
        <h2>Dagelijkse Voeding</h2>
        <div class="group-buttons">
          <BaseButton 
            @click="$router.push('/day-overview')"
            variant="primary"
            size="large"
          >
            Dag Overzicht
          </BaseButton>

          <BaseButton
            @click="$router.push('/day-analysis')"
            variant="primary"
            size="large"
            >
            Voedingsanalyse
          </BaseButton>
        </div>
      </div>
    </div>
      

      
    </div>
  </div>
</template>

<script>
import BaseButton from '../components/ui/BaseButton.vue';

export default {
  name: 'Home',
  components: {
    BaseButton
  }
}
</script>

<style scoped>
.action-groups {
  display: flex;
  gap: 32px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.action-group h2 {
  color: #1f2937;
  margin: 0;
}

.group-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recepten {
  margin-left: 1em;
}
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 48px 24px;
  text-align: center;
}

.hero h1 {
  font-size: 3rem;
  color: #1f2937;
  margin-bottom: 16px;
}

.hero p {
  font-size: 1.25rem;
  color: #6b7280;
  margin-bottom: 48px;
}

.actions {
  display: flex;
  gap: 24px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>