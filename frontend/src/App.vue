<script setup lang="ts">
import query from "./query";
import { reactive, ref, onMounted } from "vue";
import NetCat from "./components/NetCat.vue";
type Phase = "not-start" | "reading" | "in-task";

let phase = ref("not-start" as Phase);
let monitorState = ref({
  subject_id: 0,
  state: 0,
  task_index: 0,
  task_class: 0,
  mouse_distance: 0,
  mouse_click: 0,
  keyborad_press: 0,
  start_time: 0,
  data_buffer: [],
});

let isLoaded = ref(false);
let subjectID = ref(0);

onMounted(() => {
  if (isLoaded.value) {
    return;
  }

  // 同步服务器状态
  updateState();
});

let state = reactive({
  isConnected: false,
});

function updateState() {
  query.getState().then((res: any) => {
    monitorState.value = res.data;
  });

  // 未配置被试 ID
  if (monitorState.value.subject_id == 0) {
    let subjectID = prompt("请输入被试编号", "0") ?? "0";
    query.setSubjectID(parseInt(subjectID));
    updateState();
    return;
  }

  switch (monitorState.value.state) {
    case 0:
      phase.value = "not-start";
      break;
    case 1:
      phase.value = "reading";
      break;
    case 2:
      phase.value = "in-task";
      break;
  }
}

function beginWithMacOS() {}

function beginWithFigma() {}

function Next() {}
</script>

<template>
  <div class="col-start w-full text-main">
    <div class="w-full border-b-[1px] border-gray-200 p-4 row-center gap-4">
      <h1 class="text-xl text-main font-bold">🐈 &nbsp M-CAT 可用性测试终端</h1>
      <p class="text-tertiary">实验编号 {{ monitorState.subject_id }}</p>
      <div class="flex-1"></div>
      <NetCat />
    </div>

    <div v-show="phase == 'not-start'" class="flex flex-col items-center pt-36 h-full gap-12">
      <h2 class="text-4xl font-medium">请选择一个任务集开始测试</h2>

      <div class="row-center gap-12">
        <button class="big-button hover:bg-yellow-400">🍎 macOS@WIMP</button>
        <button class="big-button hover:bg-yellow-400">✏️ Figma@WIMP</button>
      </div>

      <div class="row-center gap-12">
        <button class="big-button hover:bg-yellow-400">🍎 macOS@M-CAT</button>
        <button class="big-button hover:bg-yellow-400">✏️ Figma@M-CAT</button>
      </div>
    </div>

    <pre
      class="text-sm fixed bottom-0 right-0"
    ><button @click="updateState">同步状态</button>{{ monitorState }}</pre>
  </div>
</template>

<style lang="css">
.big-button {
  @apply border-gray-200 hover:border-transparent transition-all border-[1px] p-8  text-xl font-medium rounded-full w-[240px];
}
</style>
