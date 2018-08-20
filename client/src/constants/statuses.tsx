export const CREATED = 'created';
export const RUNNING = 'running';
export const STOPPED = 'stopped';
export const FAILED = 'failed';
export const SUCCEEDED = 'succeeded';

export const isDone = (status: string): boolean => {
  return [STOPPED, FAILED, SUCCEEDED].indexOf(status) > -1;
}
