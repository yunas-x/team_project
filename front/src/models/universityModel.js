import ModelBase from "./base/modelBase";

export default class UniversityModel extends ModelBase {
    constructor(id, name, city, allProgramDataList) {
        super(id, name);

        this.city = city;
        this.allProgramDataList = allProgramDataList
    }
}