import {fetchData} from "./base/fetcher";
import {PROGRAMS_URL} from "./consts/endpoints";

const fetchPrograms = async (offset = 0, count = 20) => {
    return (await fetchData(PROGRAMS_URL, offset, count)).data.programs;
}

export {fetchPrograms};