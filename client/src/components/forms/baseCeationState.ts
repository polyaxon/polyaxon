import { splitUniqueName } from '../../constants/utils';
import { ProjectModel } from '../../models/project';

export interface BaseState {
  project: string;
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
}

export const BaseEmptyState = {
  project: '',
  tags: [],
  readme: '',
  description: '',
  name: '',
};

export const CreateEntity = (onCreate: any,
                             form: any,
                             project: string,
                             isProjectEntity: boolean,
                             projects: ProjectModel[]) => {
  if (isProjectEntity) {
      let values = ['', ''];
      if (project) {
        values = splitUniqueName(project);
      } else {
        values = splitUniqueName(projects ? projects[0].unique_name : '');
      }
      onCreate(form, values[0], values[1]);
    } else {
      onCreate(form);
    }
};
