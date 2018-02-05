export class ModalStateSchema {
  public type: string;
  public props: any;
}

export const ModalEmptyState = {
  type: '',
  props: {show: false}
};

export enum modalTypes {
  CREATE_PROJECT = 'CREATE_PROJECT',
}

export const modalPropsByTypes: {[id: string]: any} = {};
modalPropsByTypes[modalTypes.CREATE_PROJECT] = {
  show: false,
  heading: 'New Project',
  showFooter: false
};
