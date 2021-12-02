<template>
  <div
    v-if="showing"
    class="cat-card"
    :class="{ animated: animating, current: current }"
    :style="{ transform: transformString }"
  >
    <div class="cat-image" :style="{ backgroundImage: urlForBackground }">
      <div
        class="cat-image-icon"
        :class="icon.type"
        :style="{ opacity: icon.opacity }"
      ></div>
    </div>
    <div class="cat-name">Name: {{ name }}</div>
  </div>
</template>

<script>
import interact from 'interactjs';
import { nextTick } from 'vue';

export default {
  props: {
    id: { type: Number, required: true },
    picture: { type: String, required: true },
    name: { type: String },
    current: { type: Boolean, required: true },
    approved: { type: Boolean },
  },
  data() {
    return {
      showing: true,
      animating: false, // Включение анимации
      threshold: window.innerWidth / 3, // На каком расстоянии от начального положения считать карточку принятой или отклоненной
      maxRotation: 20, // Максимальный угол вращения
      position: { x: 0, y: 0, rotation: 0 },
      icon: { opacity: 0, type: null },
    };
  },
  mounted() {
    interact(this.$el).draggable({
      inertia: false,
      onstart: () => {
        this.animating = false; // Выключаем анимацию по время перетаскивания
      },
      onmove: ({ dx, dy }) => {
        // Вычисляем новые координаты
        const { position, maxRotation, threshold, icon } = this;

        const offsetX = (position.x || 0) + dx;
        const offsetY = (position.y || 0) + dy;

        position.x = offsetX;
        position.y = offsetY;

        position.rotation = maxRotation * (offsetX / threshold);
        if (position.rotation > maxRotation) {
          position.rotation = maxRotation;
        } else if (position.rotation < -maxRotation) {
          position.rotation = -maxRotation;
        }

        // По направлению смещения принимаем или отклоняем заявку.
        icon.type = "match";
        if (position.rotation < 0) {
          icon.type = "pass";
        }

        const opacityAmount = Math.abs(position.rotation) / maxRotation;
        icon.opacity = opacityAmount;
        this.$emit("draggedActive", icon.type, opacityAmount);
      },
      onend: () => {
        const { icon, position, threshold } = this;

        this.animating = true;

        icon.opacity = 1;

        // Если сдвинули на достаточое расстояние, то принимаем или отклоняем
        if (position.x > threshold) {
          this.$emit("draggedThreshold", true);
        } else if (position.x < -threshold) {
          this.$emit("draggedThreshold", false);
        } else {
          position.x = 0;
          position.y = 0;
          position.rotation = 0;
          icon.opacity = 0;
        }

        this.$emit("draggedEnded");
      },
    });
  },
  computed: {
    urlForBackground() {
      return `url(${this.picture})`;
    },
    transformString() {
      const { animating, approved, position } = this;

      if (!animating || approved !== null) {
        return `translate3D(${position.x}px, ${position.y}px, 0) rotate(${position.rotation}deg)`;
      }

      return null;
    },
  },
  watch: {
    approved() {
      const { approved, position, maxRotation, icon } = this;

      if (approved !== null) {
        // Убираем подписку на drag&drop
        interact(this.$el).unset();
        this.animating = true;

        // Двигаем карточку в заданном направлении.
        const x = window.innerWidth + window.innerWidth / 2 + this.$el.offsetWidth;

        position.x = x;
        position.rotation = maxRotation;
        icon.type = "match";

        if (!approved) {
          position.x = -x;
          position.rotation = -maxRotation;
          icon.type = "pass";
        }

        icon.opacity = 1;

        nextTick(() => {
          this.showing = false;
        });
      }
    },
  },
};
</script>

<style>
.cat-card {
  width: var(--card-width);
  height: var(--card-height);

  pointer-events: none;
  z-index: 0;
  display: none;
  left: 0;
  top: 0;
  position: absolute;
  padding: 20px;
  border-radius: 8px;
  background: var(--color-white);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  will-change: transform, opacity;
}

.cat-name {
  text-align: center;
  margin-top: 10px;
}

.cat-image {
  width: 300px;
  height: 300px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: contain;
}

.cat-image-icon {
  position: relative;
  left: 50%;
  top: 50%;
  width: var(--image-icon-size);
  height: var(--image-icon-size);
  transform: translateX(-50%) translateY(-50%);
  background: center center no-repeat transparent;
  background-size: contain;
}

/* Показываем текущую карточку */
.cat-card.current {
  pointer-events: auto;
  display: block;
  z-index: 3;
}

/* Показываем карточку под текущей */
.cat-card.current + .card {
  display: block;
  z-index: 2;
}

.cat-card.animated {
  transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.image-icon.match {
  background-image: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/617753/icon-approve.svg");
}
.image-icon.pass {
  background-image: url("https://s3-us-west-2.amazonaws.com/s.cdpn.io/617753/icon-reject.svg");
}
</style>
