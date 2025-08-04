<template>
    <div class="home">
      <div class="hero">
        <h1>Voedingswaarden App</h1>
        <p>Beheer je producten, recepten en dagelijkse voeding</p>
      </div>
  
      <div class="actions">
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
  