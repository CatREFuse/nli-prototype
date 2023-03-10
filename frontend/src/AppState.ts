import { defineStore } from 'pinia';

export const useAppState = defineStore('store', {
    state() {
        return {
            subjectID: 0,
        };
    },
});
