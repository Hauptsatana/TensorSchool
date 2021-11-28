<template>
  <div class="card" :class="cardClasses">
    <div class="card-image__container">
      <img v-bind:src="img" class="card-image__image" v-bind:alt="title" />
    </div>
    <div class="card-body">
      <h5 class="card-title" :title="title">{{ title }}</h5>
      <h4 class="card-price">{{ price }} </h4>
      <add-to-cart-btn
        ref="addBtn"
        class="card-add-btn"
        v-on:itemAdded="itemAddedHandler"
      >
      </add-to-cart-btn>
    </div>
  </div>
</template>

<script>
import AddToCartBtn from "./AddToCartBtn.vue";
import { nextTick } from "vue";
export default {
  components: { AddToCartBtn },
  props: {
    img: { type: String, default: "myPic.jpg" },
    title: String,
    price: Number
  },
  data() {
    return {
      itemAdded: false,
    };
  },
  methods: {
    itemAddedHandler(itemAdded) {
      this.itemAdded = itemAdded;
    },
  },
  computed: {
    cardClasses() {
      return { "border-warning": this.itemAdded, "border-3": this.itemAdded };
    },
  },
  mounted() {
    //   nextTick(() => {
    //       this.$refs.addBtn.$on('itemAdded', this.itemAddedHandler);
    //   });
  },
};
</script>

<style scoped>
.card {
  height: 400px;
}

.card-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-image__container {
  width: 250px;
  height: 250px;
  margin: 0 auto;
}

.card-image__image {
  max-width: 250px;
  max-height: 250px;
}

.card-add-btn {
  margin: 0 auto;
}
</style>