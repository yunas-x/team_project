import {fetchData} from "./base/fetcher";
import {UNIVERSITIES_URL} from "./consts/endpoints";

const fetchUniversities = async () => {
    return (await fetchData(UNIVERSITIES_URL)).data.universities;
}

export default fetchUniversities;