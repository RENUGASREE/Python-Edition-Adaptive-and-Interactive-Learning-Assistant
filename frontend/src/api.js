import axios from 'axios'

const API = axios.create({ baseURL: 'http://localhost:8000/api' })

API.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export async function recommend(){
  const r = await API.get('/recommendations/')
  return r.data
}

export async function gradeSubmission(problem_id, code){
  const r = await API.post('/quizattempts/', { problem_id, code })
  return r.data
}

export async function chatQuery(query){
  const r = await API.post('/chatmessages/', { message: query })
  return r.data
}

export default API
