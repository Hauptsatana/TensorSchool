<template>
  <div class="container">
    <!-- Строка поиска -->
    <div class="catalog-search-input input-group mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Поиск по названию..."
        aria-label="Поиск по названию"
        aria-describedby="catalog-search-btn"
        v-model="searchString"
      >
      <button
        class="btn btn-outline-success"
        type="button"
        id="catalog-search-btn"
      >
        Поиск
      </button>
    </div>

    <!-- Список товаров -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col item-card" v-for="item in items" :key="item.id">
        <card
          :id="item.id"
          :title="item.name"
          :img="item.photo"
          :price="item.price"
        >
        </card>
      </div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue';
import debounce from '../utils/debounce';

const SERVICE_URL = 'http://127.0.0.1:8080';
const QUERY_URL = `${SERVICE_URL}/goods`;

export default {
  data() {
    return {
      items: [],
      searchString: ''
    };
  },
  components: {
    Card,
  },
  mounted() {
    this.fetchItems();
    this.fetchItems = debounce(this.fetchItems);
  },
  watch: {
    searchString() {
      this.fetchItems();
    }
  },
  methods: {
    fetchItems() {
      let url = QUERY_URL;
      if (this.searchString) {
        url += `?search=${this.searchString}`;
      }
      fetch(url).then((response) => {
        response.json().then((result) => {
          this.items = result.result;
        })
      });
    }
  }
};
</script>

<style>
  .catalog-search-input {
    width: 400px;
  }

  .item-card {
    text-align: center;
  }
</style>