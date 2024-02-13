export function checkAreArraysEqual(arr1, arr2) {
    if (!arr1 || !arr2) {
        return false;
    }

    if (arr1.length !== arr2.length) {
        return false;
    }

    arr1.forEach((item1, i) => {
        if (JSON.stringify(item1) !== JSON.stringify(arr2[i])) {
            return false;
        }
    })

    return true;
}