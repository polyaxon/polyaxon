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
  const link = getExperimentUrl(values[0], values[1], values[2]);
  return {
    original: values[2],
    link,
    strategy: CLONING_MAPPING[strategy],
  } as CloningInterface;
}

export function getJobCloning(original: string,
                              strategy: string) {
  const values = splitUniqueName(original);
  const link = getJobUrl(values[0], values[1], values[values.length - 1]);
  return {
    original: values[2],
    link,
    strategy: CLONING_MAPPING[strategy],
  } as CloningInterface;
}
