import {fetchDataWithParams} from "./base/fetcher";
import {INFOGRAPHICS_URL} from "./consts/endpoints";

export const fetchInfographics = async (firstProgramId, secondProgramId) => {
    return (await fetchDataWithParams(INFOGRAPHICS_URL, {
        first_program_id: firstProgramId,
        second_program_id: secondProgramId,
    })).data;
}