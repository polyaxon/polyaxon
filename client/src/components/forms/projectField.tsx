import { Field } from 'formik';
import * as React from 'react';

import { ProjectModel } from '../../models/project';

export const ProjectField = (projects: ProjectModel[]) => (
  <div className="form-group">
    <label className="control-label">Project</label>
    <Field component="select" name="project" className="form-control input-sm">
      {projects.map((project: ProjectModel) => (<option key={project.unique_name}>{project.unique_name}</option>))}
    </Field>
  </div>
);
