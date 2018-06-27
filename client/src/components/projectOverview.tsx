import * as React from 'react';
import * as _ from 'lodash';

import { ProjectModel } from '../models/project';
import { getNotebookUrl, getProjectTensorboardUrl } from '../constants/utils';
import Tags from './tags';
import Description from './description';
import MetaInfo from './metaInfo/metaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import { EmptyList } from './emptyList';

export interface Props {
  project: ProjectModel;
}

function ProjectOverview({project}: Props) {
  if (_.isNil(project)) {
    return EmptyList(false, 'project', 'project');
  }
  let visibility = project.is_public ? 'Public' : 'Private';
  return (
    <div className="entity-details">
      <div className="row">
        <div className="col-md-12">
          <Description
            description={project.description}
            showEmpty={true}
          />
          <div className="meta">
            <MetaInfo
              icon="fa-lock"
              name="Visibility"
              value={visibility}
              inline={true}
            />
            <DatesMetaInfo
              createdAt={project.created_at}
              updatedAt={project.updated_at}
              inline={true}
            />
          </div>
          <div className="meta">
            <MetaInfo
              icon="fa-cube"
              name="Experiments"
              value={project.num_experiments}
              inline={true}
            />
            <MetaInfo
              icon="fa-cubes"
              name="Experiment Groups"
              value={project.num_experiment_groups}
              inline={true}
            />
             <MetaInfo
              icon="fa-tasks"
              name="Jobs"
              value={project.num_jobs}
              inline={true}
             />
             <MetaInfo
              icon="fa-cog"
              name="Builds"
              value={project.num_builds}
              inline={true}
             />
          </div>
          {project.has_tensorboard &&
          <div className="meta">
            <span className="meta-info meta-dashboard">
              <i className="fa fa-link icon" aria-hidden="true"/>
              <a href={getProjectTensorboardUrl(project.unique_name)} className="title-link">Tensorboard</a>
            </span>
          </div>
          }
          {project.has_notebook &&
          <div className="meta">
            <span className="meta-info meta-dashboard">
              <i className="fa fa-link icon" aria-hidden="true"/>
              <a href={getNotebookUrl(project.unique_name)} className="title-link">Notebook</a>
            </span>
          </div>
          }
          <Tags tags={project.tags}/>
        </div>
      </div>
    </div>
  );
}

export default ProjectOverview;
