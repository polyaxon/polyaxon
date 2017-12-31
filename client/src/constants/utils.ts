export const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

export let urlifyProjectName = function (origProjectName: string) {
    // Replaces . by /
    let re = /\./gi;
    return origProjectName.replace(re, "\/");
}

export let getCssClassForStatus = function (status?: string): string {
    if (status === 'Succeeded') {
        return 'green';
    } else if (status === 'Deleted') {
        return 'red';
    } else if (status === 'Failed') {
        return 'red';
    } else if (status === 'Created') {
        return 'light-blue';
    }
    return 'orange';
}

export let sortByUpdatedAt = function (a: any, b: any): any {
  let dateB: any = new Date(b.updated_at);
  let dateA: any = new Date(a.updated_at);
  return dateB - dateA;
}

export let pluralize = function (name: string, num_objects: number): string {
    if (num_objects !== 1) {
        return name + 's';
    }
    return name;
}