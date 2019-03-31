import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/projects';
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
import Refresh from '../refresh';
import Tags from '../tags/tags';
import GitUrl from './git';

import './intialize-instructions.less';

export interface Props {
  project: ProjectModel;
  isUpdateLoading: boolean;
  isSetGitLoading: boolean;
  UpdateErrors: any;
  setGitErrors: any;
  onFetch: () => actions.ProjectAction;
  onUpdate: (updateDict: { [key: string]: any }) => actions.ProjectAction;
  onSetGit: (updateDict: { [key: string]: any }) => actions.ProjectAction;
}

export default class ProjectOverview extends React.Component<Props, {}> {
  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const project = this.props.project;

    if (_.isNil(project)) {
      return EmptyList(false, 'project', 'project');
    }
    const visibility = project.is_public ? 'Public' : 'Private';
    return (
      <div className="entity-details">
        {!project.has_code &&
        <div className="row initialize-instructions">
          <div className="col-md-offset-2 col-md-8">
            <div className="jumbotron jumbotron-action text-center empty-jumbotron">
              <h3>This project is not initialized</h3>
              <div className="row instructions">
                <div className="col-md-6 instruction-left">
                  <h4>You can initialize this project by uploading code from you local machine.</h4>
                  <div className="instructions-section-content">
                    polyaxon init {project.name}
                  </div>
                  <h4>Upload local code to Polyaxon.</h4>
                  <div className="instructions-section-content">
                    polyaxon upload
                  </div>
                </div>
                <div className="col-md-6 instruction-right">
                  <h4>You can initialize this project by setting an external git repo.</h4>
                  <GitUrl
                    isLoading={this.props.isSetGitLoading}
                    errors={this.props.setGitErrors}
                    onSave={(git_url: string, is_public: boolean) => {
                      this.props.onSetGit({git_url, is_public});
                    }}
                  />
                  <h4>Or using Polyaxon CLI.</h4>
                  <div className="instructions-section-content">
                    polyaxon project -p {project.name} git --url="https://github.com/polyaxon/polyaxon-quick-start"
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        }
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-11">
                <Description
                  description={project.description}
                  showEmpty={true}
                  onSave={(description: string) => {
                    this.props.onUpdate({description});
                  }}
                />
              </div>
              <div className="col-md-1">
                <Refresh callback={this.refresh} pullRight={false}/>
              </div>
            </div>
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
              onSave={(tags: string[]) => {
                this.props.onUpdate({tags});
              }}
            />
            <MDEditor
              content={project.readme}
              onSave={(readme: string) => {
                this.props.onUpdate({readme});
              }}
            />
          </div>
        </div>
      </div>
    );
  }
}
