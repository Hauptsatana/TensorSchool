<template>
  <div class="statistics__container">
    <p class="statistics__approved">Approved: {{ approved }}</p>
    <p class="statistics__declined">Declined: {{ declined }}</p>
  </div>
</template>

<script>
export default {
  props: {
    approved: { type: Number, required: true },
    declined: { type: Number, required: true },
  },
};
</script>

<style>
.statistics__container {
  text-align: center;
  margin-top: 20px;
}

.statistics__approved {
  color: var(--color-green);
}

.statistics__declined {
  color: var(--color-red);
}
</style>
