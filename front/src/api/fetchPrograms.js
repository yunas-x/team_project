import {fetchData, fetchDataWithParams} from "./base/fetcher";
import {PROGRAMS_URL, FILTERED_PROGRAMS_URL} from "./consts/endpoints";

const fetchPrograms = async (offset = 0, count = 20) => {
    return (await fetchData(PROGRAMS_URL, offset, count)).data.programs;
}

const fetchFilteredPrograms = async (filterObject, offset, count) => {
    return (await fetchDataWithParams(FILTERED_PROGRAMS_URL, filterObject, offset, count)).data.programs;
}

export {fetchPrograms, fetchFilteredPrograms};