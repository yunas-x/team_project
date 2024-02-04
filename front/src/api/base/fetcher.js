import axios from "axios";

const host = axios.create({
    baseURL: process.env.REACT_APP_API_URL
})

export async function fetchData(url) {
    return await host.get(url);
}