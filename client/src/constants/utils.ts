import * as Cookies from 'js-cookie';

export const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

export let urlifyProjectName = function (origProjectName: string) {
    // Replaces . by /
    let re = /\./gi;
    return origProjectName.replace(re, "\/");
};

export let getCssClassForStatus = function (status?: string): string {
    if (status === 'Succeeded') {
        return 'success';
    } else if (status === 'Deleted') {
        return 'danger';
    } else if (status === 'Failed') {
        return 'danger';
    } else if (status === 'Created') {
        return 'info';
    }
    return 'warning';
};

export let sortByUpdatedAt = function (a: any, b: any): any {
  let dateB: any = new Date(b.updated_at);
  let dateA: any = new Date(a.updated_at);
  return dateB - dateA;
};

export let pluralize = function (name: string, num_objects: number): string {
    if (num_objects !== 1) {
        return name + 's';
    }
    return name;
};

export let isUserAuthenticated = function () {
    let hasUser = Cookies.get('user') !== undefined;
    let hasToken = Cookies.get('token') !== undefined;
    return (hasUser && hasToken);
};

export let getStoredToken = function () {
    return Cookies.get('token');
};

export let getHomeUrl = function () {
    let user = Cookies.get('user');
    return `/${user}/`;
};

export let getLoginUrl = function () {
    return '/auth/login/';
};

export let getLogoutUrl = function () {
    return '/auth/logout/';
};
