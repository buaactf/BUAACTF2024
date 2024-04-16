<template>
  <span v-if="!number || skip"><span v-bind="leaves" v-html="enabled ? character : choice"></span></span>
  <span v-else>
    <!-- create child with total number -->
    <!-- set prop enabled for control -->
    <!-- set prop removed for control -->
    <character-field v-for="i in total" :key="i" v-bind="bind(i)" />
  </span>
</template>

<script setup>
import { hide, show } from './styles';

const props = defineProps({
  character: { type: String, required: true },
  enabled: { type: Boolean, required: true },
  removed: { type: Boolean, required: true },
  maxitems: { type: Number, required: true },
  minitems: { type: Number, required: true },
  number: { type: Number, required: true }
});

const skip = props.number > 2 && Math.random() < 0.5;
const lhs = parseInt(Math.random() * (props.maxitems - props.minitems + 1) + props.minitems, 10);
const rhs = parseInt(Math.random() * (props.maxitems - props.minitems + 1) + props.minitems, 10);
const total = Math.max(lhs, rhs); // total child character-field count
const index = Math.min(lhs, rhs); // right child character-field index

const upperGetter = () => 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.charAt(Math.floor(Math.random() * 26));
const lowerGetter = () => 'abcdefghijklmnopqrstuvwxyz'.charAt(Math.floor(Math.random() * 26));
const choice = Math.random() < 0.5 ? upperGetter() : lowerGetter();
const showGetter = () => show[parseInt(Math.random() * show.length, 10)];
const hideGetter = () => hide[parseInt(Math.random() * hide.length, 10)];
const leaves = /* determine whether to display character */ {
  class: props.removed || props.enabled ? showGetter() : hideGetter(),
  // style: { userSelect: 'auto' }
  // style: { userSelect: 'none' }
  style: { userSelect: 'none' /* disable selection */ }
};

const bind = (i) => {
  const enabled = props.enabled && (i === index || Math.random() < -0.2);
  const removed = props.removed || (i !== index && Math.random() < +0.2);
  const lhs = hideGetter();
  const rhs = showGetter();
  return {
    number: parseInt(Math.random() * props.number, 10),
    maxitems: props.maxitems,
    minitems: props.minitems,
    class: removed !== props.removed ? lhs : rhs,
    enabled: enabled,
    removed: removed,
    character: props.character
  };
};
</script>
