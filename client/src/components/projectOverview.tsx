import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';

import { ProjectModel } from '../models/project';
import { getNotebookUrl, getTensorboardUrl } from '../constants/utils';
import Tags from './tags';
import Description from './description';

export interface Props {
  project: ProjectModel;
}

function ProjectOverview({project}: Props) {
  if (_.isNil(project)) {
    return (<div>Nothing</div>);
  }
  let visibility = project.is_public ? 'Public' : 'Private';
  return (
    <div className="entity-details">
      <div className="row">
        <div className="col-md-10 col-md-offset-1">
          <div className="entity-name">{project.name}</div>
          <div className="meta text-center">
                <span className="meta-info">
                  <i className="fa fa-lock icon" aria-hidden="true"/>
                  <span className="title">Visibility:</span>
                  {visibility}
                </span>
            <span className="meta-info">
                  <i className="fa fa-clock-o icon" aria-hidden="true"/>
                  <span className="title">Last updated:</span>
              {moment(project.updated_at).fromNow()}
                </span>
            <span className="meta-info">
                  <i className="fa fa-cube icon" aria-hidden="true"/>
                  <span className="title">Experiments:</span>
              {project.num_experiments}
                </span>
            <span className="meta-info">
                  <i className="fa fa-cubes icon" aria-hidden="true"/>
                  <span className="title">Experiment Groups:</span>
              {project.num_experiment_groups}
                </span>
          </div>
          <div className="text-center"><Tags tags={project.tags}/></div>
          <Description
            description={project.description}
            entity="project"
            command="polyaxon project update --description=..."
          />
          <div className="meta">
            {project.has_tensorboard &&
            <span className="meta-info meta-dashboard">
                  <i className="fa fa-link icon" aria-hidden="true"/>
                  <a href={getTensorboardUrl(project.user, project.name)} className="title-link">Tensorboard</a>
                </span>
            }
            {project.has_notebook &&
            <span className="meta-info meta-dashboard">
                  <i className="fa fa-link icon" aria-hidden="true"/>
                  <a href={getNotebookUrl(project.user, project.name)} className="title-link">Notebook</a>
                </span>
            }
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProjectOverview;
