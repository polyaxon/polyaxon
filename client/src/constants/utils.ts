export const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

export let urlifyProjectName = function (origProjectName: string) {
    // Replaces . by /
    let re = /\./gi;
    return origProjectName.replace(re, "\/");
}