import * as Cookies from 'js-cookie';
import {TokenStateSchema} from "../models/token";

export const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

export let urlifyProjectName = function (projectName: string) {
    // Replaces . by /
    let re = /\./gi;
    return projectName.replace(re, "\/");
};

export let splitProjectName  = function (projectName: string) {
    return projectName.split('.');
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

export let getToken = function(): TokenStateSchema | null {
    let user = Cookies.get('user');
    let token = Cookies.get('token');
    if (user !== undefined && token !== undefined) {
        return {token: token, user: user};
    }
    return null;
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
    return `/app/${user}/`;
};

export let getLoginUrl = function () {
    return '/app/auth/login/';
};

export let getLogoutUrl = function () {
    return '/app/auth/logout/';
};

export let getProjectUrl = function (username: string, projectName: string) {
    return `/app/${username}/${projectName}`
};

export let getGroupUrl = function (username: string, projectName: string, groupSequence: number) {
    let projectUrl = getProjectUrl(username, projectName);
    return `${projectUrl}/groups/${groupSequence}/`
};

export let getExperimentUrl = function (username: string, projectName: string, experimentSequence: number) {
    let projectUrl = getProjectUrl(username, projectName);
    return `${projectUrl}/experiments/${experimentSequence}/`
};
