import { BASE_API_URL } from '../constants/api';
import { urlifyProjectName } from '../constants/utils';

export function outputsDownloadUrl(projectUniqueName: string,
                                   resources: string,
                                   id: number) {
  return `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/outputs/download`;
}

export function logsDownloadUrl(projectUniqueName: string,
                                resources: string,
                                id: number) {
  return `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/logs`;
}

export function downloadName(projectUniqueName: string,
                             resources: string,
                             id: number) {
  return `${projectUniqueName}.${resources}.${id}`;
}

