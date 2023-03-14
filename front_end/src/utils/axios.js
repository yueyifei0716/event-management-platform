import axios from "axios";
import message from './messages'


const instance = axios.create({
    baseURL: 'http://127.0.0.1:5000'
});

instance.interceptors.response.use(response => {
    console.log(response, 'axios response');
    if (response.status === 200) {
        return response;
    } else {
        return Promise.reject(response);
    }

}, error => {
    // if server not response, throw a error
    let msg = error && error.response && error.response.data && error.response.data.message;
    // else throw backend error
    message.error({ content: msg || 'System error, please run Server', duration: 3500 });
    return Promise.reject(error.response);

});

export default instance;