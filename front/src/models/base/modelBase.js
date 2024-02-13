export default class ModelBase {
    constructor(id, name, displayName = undefined) {
        this.id = id;
        this.name = name;
        this.displayName = displayName ?? name;
    }
}