export const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

export let urlifyProjectName = function (origProjectName: string) {
    // Replaces . by /
    let re = /\./gi;
    return origProjectName.replace(re, "\/");
}

export let getCssClassForStatus = function (status?: string): string {
    if (status === 'Succeeded') {
        return 'green';
    } else if (status === 'Running') {
        return 'orange';
    } else if (status === 'Starting') {
        return 'orange';
    } else if (status === 'Deleted') {
        return 'red';
    } else if (status === 'Failed') {
        return 'red';
    }
    return '';
}

export let sortByCreatedAt = function (a: any, b: any): any {
  let dateB: any = new Date(b.created_at);
  let dateA: any = new Date(a.created_at);
  return dateB - dateA;
}