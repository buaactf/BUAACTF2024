<template>
  <div style="user-select: none">
    <h1>Can You Copy Me?</h1>
    <!-- ---------------------------------------------------------------- -->
    <div>下面两部分中涉及到 1024 个大写或小写字母，你需要计算这个长为 1024 的字符串的 SHA256 并拼接到 flag 中：</div>
    <div style="margin: 5px"></div>
    <div>{{ payload.flag }}</div>
    <div style="margin: 5px"></div>
    <div>请注意不要包含空白字符，包括但不限于行首空格和行末换行；请注意 SHA256 使用大写 HEX 编码，共 64 个字符！</div>
    <div>请注意不要包含空白字符，包括但不限于行首空格和行末换行；请注意 SHA256 使用大写 HEX 编码，共 64 个字符！</div>
    <div>请注意不要包含空白字符，包括但不限于行首空格和行末换行；请注意 SHA256 使用大写 HEX 编码，共 64 个字符！</div>
    <!-- ---------------------------------------------------------------- -->
    <div style="margin: 20px"></div>
    <div style="height: 1px; background-color: black"></div>
    <div style="margin: 20px"></div>
    <div>第一部分：下面有四行字符串，每一行的字符串都包含 128 个字符，但是屏幕宽度有限，一些字符你可能无法看到，</div>
    <div>你需要想办法拿到这些字符串（共计 512 个字符，均为大写或小写字母，不含空白字符）用于计算 flag 的值：</div>
    <div style="margin: 15px"></div>
    <div :style="style1">
      <div><character-field v-for="(i, id) in payload.part1[0]" :key="id" :character="i" v-bind="bind" /></div>
      <div><character-field v-for="(i, id) in payload.part1[1]" :key="id" :character="i" v-bind="bind" /></div>
      <div><character-field v-for="(i, id) in payload.part1[2]" :key="id" :character="i" v-bind="bind" /></div>
      <div><character-field v-for="(i, id) in payload.part1[3]" :key="id" :character="i" v-bind="bind" /></div>
    </div>
    <!-- ---------------------------------------------------------------- -->
    <div style="margin: 20px"></div>
    <div style="height: 1px; background-color: black"></div>
    <div style="margin: 20px"></div>
    <div>第二部分：下面有四行字符串，每一行的字符串都包含 128 个字符，但是屏幕宽度有限，一些字符你可能无法看到，</div>
    <div>你需要想办法拿到这些字符串（共计 512 个字符，均为大写或小写字母，不含空白字符）用于计算 flag 的值：</div>
    <div style="margin: 10px"></div>
    <div :style="style2">
      <div><canvas ref="canvas1" width="720" height="24" :style="canvas"></canvas></div>
      <div><canvas ref="canvas2" width="720" height="24" :style="canvas"></canvas></div>
      <div><canvas ref="canvas3" width="720" height="24" :style="canvas"></canvas></div>
      <div><canvas ref="canvas4" width="720" height="24" :style="canvas"></canvas></div>
    </div>
    <!-- ---------------------------------------------------------------- -->
    <div style="margin: 20px"></div>
    <div style="height: 1px; background-color: black"></div>
    <div style="margin: 20px"></div>
    <div>最后，如果你对浏览器反调试技术感兴趣，可以看看 <a :href="payload.href">U Can't Debug This</a> 这篇文章，以及：</div>
    <div>请注意不要包含空白字符，包括但不限于行首空格和行末换行；请注意 SHA256 使用大写 HEX 编码，共 64 个字符！（再次）</div>
    <div>请注意不要包含空白字符，包括但不限于行首空格和行末换行；请注意 SHA256 使用大写 HEX 编码，共 64 个字符！（再次）</div>
    <div>请注意不要包含空白字符，包括但不限于行首空格和行末换行；请注意 SHA256 使用大写 HEX 编码，共 64 个字符！（再次）</div>
  </div>
</template>

<script setup>
import CharacterField from './CharacterField.vue';
import { payload } from './flag';

payload.href; // assert field exists
payload.part1; // assert field exists
payload.part2; // assert field exists
payload.flag; // assert field exists

const bind = { minitems: 1, maxitems: 3, enabled: !!1, removed: !!0, number: 4 };
const canvas = { margin: 'auto', height: '24px' };
const style1 = { font: '24px Georgia', margin: 'auto', width: '720px', overflow: 'hidden' };
const style2 = { font: '24px Georgia', margin: 'auto', width: '720px', overflow: 'hidden' };

// ----------------------------------------------------------------

import DisableDevtool from 'disable-devtool';
import { onMounted, ref } from 'vue';

DisableDevtool({ ondevtoolopen: () => (location.href = 'https://www.bilibili.com/video/BV1GJ411x7h7/') });
const canvas1 = ref(undefined);
const canvas2 = ref(undefined);
const canvas3 = ref(undefined);
const canvas4 = ref(undefined);

onMounted(() => {
  const scale = window.devicePixelRatio;
  canvas1.value.width = canvas2.value.width = Math.round(720 * scale);
  canvas3.value.width = canvas4.value.width = Math.round(720 * scale);
  canvas1.value.height = canvas2.value.height = Math.round(24 * scale);
  canvas3.value.height = canvas4.value.height = Math.round(24 * scale);
  const context1 = canvas1.value.getContext('2d');
  const context2 = canvas2.value.getContext('2d');
  const context3 = canvas3.value.getContext('2d');
  const context4 = canvas4.value.getContext('2d');
  context1.font = context2.font = '24px Georgia';
  context3.font = context4.font = '24px Georgia';
  context1.scale(scale, scale); // solve display blurring qwq
  context2.scale(scale, scale); // solve display blurring qwq
  context3.scale(scale, scale); // solve display blurring qwq
  context4.scale(scale, scale); // solve display blurring qwq
  context1.fillText(payload.part2[0], 0, 24);
  context2.fillText(payload.part2[1], 0, 24);
  context3.fillText(payload.part2[2], 0, 24);
  context4.fillText(payload.part2[3], 0, 24);
});
</script>
