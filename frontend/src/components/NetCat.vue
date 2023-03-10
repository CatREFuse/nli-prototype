<script setup lang="ts">
import query from "../query";
import { ref, onMounted } from "vue";

type NetState = "connecting" | "connected" | "disconnected";

let netState = ref("disconnected" as NetState);

onMounted(() => {
  connect();
});

function connect() {
  netState.value = "connecting";
  query
    .connect()
    .then((res) => {
      res.data == "M-CAT"
        ? (netState.value = "connected")
        : (netState.value = "disconnected");
    })
    .catch((res) => {
      netState.value = "disconnected";
    });
}

function setBaseURL() {
  query.axios.defaults.baseURL =
    prompt("请输入数据端链接", query.axios.defaults.baseURL) ?? "";
  connect();
}
</script>

<template>
  <div class="row-center gap-2 transition-colors">
    <div class="row-center gap-1">
      <div
        class="w-[6px] h-[6px] rounded-full bg-green-600"
        :class="
          netState === 'connecting'
            ? 'animate-pulse bg-yellow-500'
            : netState === 'connected'
            ? 'bg-green-600'
            : netState === 'disconnected'
            ? 'bg-red-600'
            : ''
        "
      ></div>
      <div
        class="text-green-600 text-sm"
        :class="
          netState === 'connecting'
            ? 'animate-pulse text-yellow-500'
            : netState === 'connected'
            ? 'text-green-600'
            : netState === 'disconnected'
            ? 'text-red-600'
            : ''
        "
      >
        {{
          netState === "connecting"
            ? "连接中"
            : netState === "connected"
            ? "已连接"
            : netState === "disconnected"
            ? "未连接"
            : ""
        }}
      </div>
    </div>
    <button
      class="text-tertiary hover:text-secondary border-gray-200 hover:border-gray-300 border-[1px] p-1 px-3 rounded-full row-center gap-2 outline-none"
      @click="setBaseURL"
    >
      <div>配置网络</div>
    </button>
  </div>
</template>

<style lang="css"></style>
