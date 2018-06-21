import * as React from 'react';
import * as _ from 'lodash';

import { ProjectModel } from '../models/project';
import { getNotebookUrl, getTensorboardUrl } from '../constants/utils';
import Tags from './tags';
import Description from './description';
import MetaInfo from './metaInfo/metaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';

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
        <div className="col-md-12">
          <Description
            description={project.description}
            entity="project"
            command="polyaxon project update --description=..."
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
          <Tags tags={project.tags}/>
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
