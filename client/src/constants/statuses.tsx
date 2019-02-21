export const CREATED = 'created';
export const RUNNING = 'running';
export const STOPPED = 'stopped';
export const STOPPING = 'stopping';
export const FAILED = 'failed';
export const SUCCEEDED = 'succeeded';
export const DONE = 'done';
export const WARNING = 'warning';

export const isDone = (status: string): boolean => {
  return [STOPPED, FAILED, SUCCEEDED, DONE].indexOf(status) > -1;
};
