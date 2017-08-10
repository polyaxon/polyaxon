export class ModalStateSchema {
  public type: string;
  public props: any;
}

export const ModalEmptyState = {
  type: '',
  props: {show: false}
};

export enum modalTypes {
  CREATE_PROJECT='CREATE_PROJECT',
}

