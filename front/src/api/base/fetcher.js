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

export async function fetchDataWithParams(url, params) {
    return await host.get(url, {
        params: params,
    })
}

/**
 * Performs POST request
 */
export async function fetchDataWithPOST(url, data) {
    return await host.post(url, data)
}