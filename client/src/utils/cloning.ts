import { getExperimentUrl, getJobUrl, splitUniqueName } from '../constants/utils';
import { CloningInterface } from '../interfaces/cloning';

const CLONING_MAPPING = {
  resume: 'Resumed from',
  clone: 'Cloned from',
  restart: 'Restarted from',
} as { [key: string]: string };

export function getExperimentCloning(original: string,
                                     strategy: string) {
  const values = splitUniqueName(original);
  const originalExperiment = values[values.length - 1];
  const link = getExperimentUrl(values[0], values[1], originalExperiment);
  return {
    original: originalExperiment,
    link,
    strategy: CLONING_MAPPING[strategy],
  } as CloningInterface;
}

export function getJobCloning(original: string,
                              strategy: string) {
  const values = splitUniqueName(original);
  const originalJob = values[values.length - 1];
  const link = getJobUrl(values[0], values[1], originalJob);
  return {
    original: originalJob,
    link,
    strategy: CLONING_MAPPING[strategy],
  } as CloningInterface;
}
