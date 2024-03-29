import {fetchData} from "./base/fetcher";
import {FIELDS_OF_STUDY_URL} from "./consts/endpoints";

const fetchFieldsOfStudy = async (offset = 0, count = 20) => {
    return (await fetchData(FIELDS_OF_STUDY_URL, offset, count)).data.fields_of_study;
}

export default fetchFieldsOfStudy;