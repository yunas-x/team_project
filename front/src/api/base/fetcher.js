import axios from "axios";

const host = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    headers: { Authorization: `Bearer ${process.env.REACT_APP_AUTH_TOKEN}` }
})

/**
 * Performs GET request
 */
export async function fetchData(url, offset = 0, limit = 20) {
    return await host.get(url, {
        params: {
            offset: offset,
            limit: limit,
        }
    });
}

/**
 * Performs POST request
 */
export async function fetchDataWithParams(url, data, offset = 0, limit = 20) {
    return await host.post(url, data, {
        params: {
            offset: offset,
            limit: limit,
        }
    })
}