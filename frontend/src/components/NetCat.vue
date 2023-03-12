<script setup lang="ts">
import query from "../query";
import { ref, onMounted } from "vue";
import axios from "axios";

type NetState = "connecting" | "connected" | "disconnected";

let netState = ref("disconnected" as NetState);

let url = ref("");
onMounted(() => {
  // 获取当前地址栏地址
  url.value = window.location.origin;
  // 去除端口号
  url.value = url.value.replace(/:\d+/, "");
  query.axios.defaults.baseURL = url.value + ":8848";
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
    prompt("请输入数据端链接（刷新自动获取）", query.axios.defaults.baseURL) ?? "";
  connect();
}
</script>

<template>
  <div class="row-center gap-2 transition-colors">
    <!-- {{ url }} -->
    <div
      class="row-center gap-1 line-button"
      :class="
        netState === 'connecting'
          ? 'animate-pulse border-yellow-400'
          : netState === 'connected'
          ? 'border-green-600'
          : netState === 'disconnected'
          ? 'border-red-500'
          : ''
      "
      @click="setBaseURL"
    >
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
        class="text-green-600 text-sm font-medium"
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
  </div>
</template>

<style lang="css"></style>
