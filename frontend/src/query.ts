import axios from 'axios';

if (import.meta.env.DEV) {
    axios.defaults.baseURL = 'http://127.0.0.1:8848'; // 测试环境下服务器
} else {
    axios.defaults.baseURL = ''; // 正式环境下本地服务器
}

export default {
    reset: () => axios.get('/reset'),
    getState: () => axios.get('/state'),
    setSubjectID: (id: number)=>axios.post(`/set-subject-id/${id}`),
    start: (taskClassID: number) => axios.get(`/start/${taskClassID}`),
    beginTask: axios.get('/begin-task'),
    next: () => axios.get('/next'),
    connect: () => axios.get('/'),
    axios,
};
