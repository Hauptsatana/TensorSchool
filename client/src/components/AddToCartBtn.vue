<template>
<div class="add-to-cart-btn__container">
    <button
        class="btn btn-warning add-to-cart-btn__btn"
        v-if="count === 0"
        v-on:click="addToCart"
    >
        В корзину
    </button>
    <div v-else class="input-group">
        <button class="btn btn-warning" v-on:click="count--">-</button>
        <input class="form-control" type="text" v-model="count" />
        <button class="btn btn-warning" v-on:click="addToCart">+</button>
    </div>
</div>
</template>

<script>
export default {
    props: {
        title: String
    },
    data() {
        return {
            count: 0
        }
    },
    methods: {
        addToCart() {
            this.count++;
        }
    },
    watch: {
        count(newValue, oldValue) {
            const itemAdded = newValue > 0;
            this.$emit('itemAdded', itemAdded);
        }
    }
};
</script>

<style>
.add-to-cart-btn__container {
    width: 200px;
    margin-bottom: 30px;
}

.add-to-cart-btn__btn {
    width: 100%;
}
</style>