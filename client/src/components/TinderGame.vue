<template>
  <div class="tinder__container">
    <div class="center">
      <div class="cat-card__container">
        <tinder-card
          v-for="(cat, index) in cats.data"
          :key="cat.id"
          :id="cat.id"
          :picture="cat.picture"
          :name="cat.name"
          :approved="cat.approved"
          :current="index === cats.index"
          @draggedThreshold="setApproval"
        />
      </div>
      <tinder-statistics :approved="approved" :declined="declined" />
    </div>
  </div>
</template>

<script>
import { cats as catsLocal } from "../utils/localData";
import TinderCard from "./TinderCard.vue";
import TinderStatistics from "./TinderStatistics.vue";

export default {
  components: {
    TinderCard,
    TinderStatistics,
  },
  data() {
    return {
      cats: {
        data: null,
        index: 0,
        limit: 10,
      },
      index: 0,
      approved: 0,
      declined: 0,
    };
  },
  methods: {
    getData() {
      const cats = this.cats;
      cats.data = null;

      return this.getDataLocal().then((arrayData) => {
        this.cats.data = arrayData;
      });
    },
    getDataRemote() {
      return fetch(
        `https://virtserver.swaggerhub.com/IntroLesson/intro_lesson/v1/cats?limit=5`
      )
        .then((response) => {
          return response.json();
        })
        .then((result) => {
          return result.results;
        });
    },
    getDataLocal() {
      return Promise.resolve(catsLocal);
    },
    setApproval(approved) {
      // Проставляем статус у карточки, идем за новыми данными, если карточки кончились
      const cats = this.cats;

      cats.data[cats.index].approved = approved;
      if (approved) {
        this.approved++;
      } else {
        this.declined++;
      }

      cats.index++;

      // Закончили эту страницу - переходим к следующей
      if (cats.index >= cats.data.length) {
        cats.page++;
        cats.index = 0;
        this.getData();
      }
    },
  },
  mounted() {
    this.getData();
  },
};
</script>

<style>
:root {
  --card-width: 340px;
  --card-height: 380px;
  --card-padding: 10px;

  --image-icon-size: 200px;

  --color-white: #fff;
  --color-orange: #f0a435;
  --color-grey: #6e6e6e;
  --color-text: #444;
  --color-background: #f3f3f3;
  --color-green: #069922;
  --color-red: #d04d4d;
}

.center {
  width: var(--card-width);
  position: relative;
  margin: 0 auto;
  top: 50%;
  transform: translateY(-50%);
}

.cat-card__container {
  position: relative;
  width: var(--card-width);
  height: var(--card-height);
}

.tinder__container {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}
</style>
