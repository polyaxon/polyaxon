export const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

export let urlifyProjectName = function (origProjectName: string) {
    // Replaces . by /
    let re = /\./gi;
    return origProjectName.replace(re, "\/");
}

export let getCssClassForStatus = function (status?: string): string {
    if (status === 'Succeeded') {
        return 'green';
    } else if (status === 'Building') {
        return 'orange';
    } else if (status === 'Scheduling') {
        return 'orange';
    } else if (status === 'UNKNOWN') {
        return 'orange';
    } else if (status === 'Deleted') {
        return 'red';
    } else if (status === 'Failed') {
        return 'red';
    } else if (status === 'Created') {
        return 'light-blue';
    } else if (status === 'Running') {
        return 'orange';
    } else if (status === 'Starting') {
        return 'orange';
    }
    return '';
}

export let sortByUpdatedAt = function (a: any, b: any): any {
  let dateB: any = new Date(b.updated_at);
  let dateA: any = new Date(a.updated_at);
  return dateB - dateA;
}