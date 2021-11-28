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
    <div
      v-if="items && items.length > 0"
      class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div class="col" v-for="item in items" :key="item.id">
        <card
          :id="item.id"
          :title="item.name"
          :img="item.photo"
          :price="item.price"
        >
        </card>
      </div>
    </div>
    <!-- Пустые результаты -->
    <div v-else class="catalog-list__empty">
      Товары не найдены. Измените параметры поиска.
    </div>
  </div>
</template>

<script>
import Card from './Card.vue';
import debounce from '../utils/debounce';
import { phones } from '../utils/localData';

const SERVICE_URL = 'http://127.0.0.1:8080';
const QUERY_URL = `${SERVICE_URL}/goods`;

/**
 * Получить товары с бека.
 */
function fetchRemoteItems(searchString) {
  let url = QUERY_URL;
  if (searchString) {
    url += `?search=${searchString}`;
  }
  return fetch(url).then((response) => {
    return response.json().then((result) => {
      return result.result;
    })
  });
}

/**
 * Получить товары с локального хранилища.
 */
function fetchLocalItems(searchString) {
  return Promise.resolve(phones).then((items) => {
    if (!searchString) {
      return items;
    }

    // Фильтруем по названию.
    const lowerSearchString = searchString.toLowerCase();
    return items.filter((item) => {
      return item.name.toLowerCase().includes(lowerSearchString);
    })
  });
}

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
    this.refreshItems();

    // Объединяем вызовы бекенда, если они происходят чаще, чем раз в полсекунды.
    // Можно закомментировать эту строку и посмотреть, как ухудшился UX
    this.refreshItems = debounce(this.refreshItems, 500);
  },
  watch: {
    searchString() {
      this.refreshItems();
    }
  },
  methods: {
    /**
     * Обновление списка товаров.
     */
    refreshItems() {
      let fetchMethod = fetchLocalItems;

      // Раскомментируйте строчку, если нужны запросы к беку.
      fetchMethod = fetchRemoteItems;

      fetchMethod(this.searchString).then((fetchedItems) => {
        this.items = fetchedItems
      })
    }
  }
};
</script>

<style>
  .catalog-search-input {
    width: 400px;
  }

  .catalog-list__empty {
    text-align: center;
    font-size: 20px;
    color: gray;
    margin-top: 50px;
  }
</style>
