import {fetchData} from "./base/fetcher";
import {FIELDS_OF_STUDY_URL} from "./consts/endpoints";

const fetchFieldsOfStudy = async (offset, count) => {
    return (await fetchData(FIELDS_OF_STUDY_URL, offset, count)).data;
}

export default fetchFieldsOfStudy;