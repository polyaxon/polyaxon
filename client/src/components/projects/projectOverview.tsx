import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/project';
import { getNotebookUrl, getProjectTensorboardUrl } from '../../constants/utils';
import { ProjectModel } from '../../models/project';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import MDEditor from '../mdEditor/mdEditor';
import BuildCountMetaInfo from '../metaInfo/counts/buildCountMetaInfo';
import ExperimentCountMetaInfo from '../metaInfo/counts/experimentCountMetaInfo';
import GroupCountMetaInfo from '../metaInfo/counts/groupCountMetaInfo';
import JobCountMetaInfo from '../metaInfo/counts/jobCountMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import MetaInfo from '../metaInfo/metaInfo';
import Tags from '../tags';

export interface Props {
  project: ProjectModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.ProjectAction;
}

export default class ProjectOverview extends React.Component<Props, {}> {
  public render() {
    const project = this.props.project;
    if (_.isNil(project)) {
      return EmptyList(false, 'project', 'project');
    }
    const visibility = project.is_public ? 'Public' : 'Private';
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <Description
              description={project.description}
              showEmpty={true}
              onSave={(description: string) =>  { this.props.onUpdate({description}); }}
            />
            <div className="meta">
              <MetaInfo
                icon="fas fa-unlock-alt"
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
              <ExperimentCountMetaInfo
                count={project.num_experiments}
                inline={true}
              />
              <GroupCountMetaInfo
                count={project.num_experiment_groups}
                inline={true}
              />
              <JobCountMetaInfo
                count={project.num_jobs}
                inline={true}
              />
              <BuildCountMetaInfo
                count={project.num_builds}
                inline={true}
              />
            </div>
            {project.has_tensorboard &&
            <div className="meta">
            <span className="meta-info meta-dashboard">
              <i className="fas fa-link icon" aria-hidden="true"/>
              <a href={getProjectTensorboardUrl(project.unique_name)} className="title-link">Tensorboard</a>
            </span>
            </div>
            }
            {project.has_notebook &&
            <div className="meta">
            <span className="meta-info meta-dashboard">
              <i className="fas fa-link icon" aria-hidden="true"/>
              <a href={getNotebookUrl(project.unique_name)} className="title-link">Notebook</a>
            </span>
            </div>
            }
            <Tags
              tags={project.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
            <MDEditor
              content={project.readme}
              onSave={(readme: string) => { this.props.onUpdate({readme}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
