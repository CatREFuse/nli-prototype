<script setup lang="ts">
import query from "./query";
import { reactive, ref, onMounted, computed } from "vue";
import NetCat from "./components/NetCat.vue";
type Phase = "not-start" | "reading" | "in-task";

let phase = ref("not-start" as Phase);
let monitorState = ref({
  subject_id: 0,
  state: 0,
  task_round: 0,
  task_index: 0,
  task_class: 0,
  mouse_distance: 0,
  mouse_click: 0,
  keyborad_press: 0,
  start_time: 0,
  data_buffer: [],
});

let isLoaded = ref(false);
let macOSSet = ref([] as string[]);
let FigmaSet = ref([] as string[]);

let taskList = computed(() => {
  if (monitorState.value.task_class == 0) {
    return macOSSet.value;
  } else {
    return FigmaSet.value;
  }
});

onMounted(() => {
  if (isLoaded.value) {
    return;
  }

  // 同步服务器状态
  updateState();
  isLoaded.value = true;
  query.getMacOSSet().then((res: any) => {
    macOSSet.value = res.data;
  });
  query.getFigmaSet().then((res: any) => {
    FigmaSet.value = res.data;
  });
});

let state = reactive({
  isConnected: false,
});

async function updateState() {
  query.getState().then((res: any) => {
    monitorState.value = res.data;
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
  });
}

async function start(taskRound: number, taskClass: number) {
  if (monitorState.value.subject_id == 0) {
    alert("请输入实验编号");
    return;
  }
  await query.start(taskRound, taskClass);
  updateState();
}

async function beginTask() {
  await query.beginTask();
  updateState();
}

async function next() {
  if (monitorState.value.task_index == 5) {
    if (monitorState.value.task_class == 1 && monitorState.value.task_round == 1) {
      alert("最后一个实验已完成, 实验编号已重置");
    } else {
      alert("实验已完成");
    }
  }
  await query.next();
  updateState();
}

async function reset() {
  await query.reset();
  let subjectID = prompt("请输入被试编号", "0") ?? "0";
  await query.setSubjectID(parseInt(subjectID));
  updateState();
}
</script>

<template>
  <div class="col-start w-full text-main select-none">
    <div class="w-full border-b-[1px] border-gray-200 p-4 row-center gap-4">
      <h1 class="text-xl text-main font-bold">🐈 &nbsp M-CAT 可用性测试终端</h1>
      <p v-if="monitorState.subject_id != 0">实验编号 {{ monitorState.subject_id }}</p>
      <button v-if="monitorState.subject_id != 0" class="line-button" @click="reset">
        重置
      </button>
      <button v-else @click="reset" class="line-button">请输入实验编号</button>
      <div class="flex-1"></div>
      <NetCat />
    </div>

    <!-- not-start -->
    <div
      v-show="phase == 'not-start'"
      class="flex flex-col items-center pt-36 h-full gap-12 font-mono"
    >
      <h2 class="text-4xl font-medium">请选择一个任务集开始测试</h2>

      <div class="row-center gap-12">
        <button @click="start(0, 0)" class="big-button hover:bg-yellow-400">
          🍎 macOS@WIMP
        </button>
        <button @click="start(0, 1)" class="big-button hover:bg-yellow-400">
          🎨 Figma@WIMP
        </button>
      </div>

      <div class="row-center gap-12">
        <button @click="start(1, 0)" class="big-button hover:bg-yellow-400">
          🍎 macOS@M-CAT
        </button>
        <button @click="start(1, 1)" class="big-button hover:bg-yellow-400">
          🎨 Figma@M-CAT
        </button>
      </div>
    </div>

    <!-- reading -->
    <div v-if="phase == 'reading'" class="col-center pt-32 text-center gap-8">
      <h1 class="text-gray-400 text-xl">请阅读任务要求，准备好后点击开始</h1>
      <p class="text-2xl text-main w-[50%] h-[72px]">
        {{ taskList[monitorState.task_index] }}
      </p>
      <button class="opt-button bg-yellow-400" @click="beginTask">开始操作</button>
    </div>

    <!-- in-task -->
    <div v-if="phase == 'in-task'" class="col-center pt-32 text-center gap-8">
      <h1 class="text-main text-xl font-bold">请进行任务操作</h1>
      <p class="text-2xl text-gray-400 w-[50%] h-[72px]">
        {{ taskList[monitorState.task_index] }}
      </p>
      <button class="opt-button bg-blue-500 text-white" @click="next">
        完成任务，进行下一个
      </button>
    </div>

    <!-- indicator -->
    <div
      v-if="phase != 'not-start'"
      class="fixed w-full bottom-8 text-2xl col-center font-bold font-mono text-gray-400"
    >
      <div>{{ monitorState.task_index + 1 }} / 6</div>
    </div>

    <!-- <pre
      class="text-sm fixed bottom-0 right-0"
    ><button @click="updateState">同步状态</button>{{ monitorState }}</pre> -->
  </div>
</template>

<style lang="css">
.big-button {
  @apply border-gray-200 hover:border-transparent transition-all border-[1px] p-8  text-xl font-medium rounded-full w-[240px];
}

.line-button {
  @apply text-tertiary hover:text-secondary  border-[1px] p-1 px-3 rounded-full row-center gap-2 outline-none;
}

.opt-button {
  @apply text-xl rounded-full py-2 px-5 outline-none font-medium hover:shadow-lg transition-shadow;
}
</style>
