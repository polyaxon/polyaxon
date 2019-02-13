import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/project';
import { getProjectUrl, getUserUrl } from '../../constants/utils';
import ActivityLogs from '../../containers/activityLogs';
import Builds from '../../containers/builds';
import Experiments from '../../containers/experiments';
import Groups from '../../containers/groups';
import Jobs from '../../containers/jobs';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { ProjectModel } from '../../models/project';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import { EmptyList } from '../empty/emptyList';
import ProjectInstructions from '../instructions/projectInstructions';
import LinkedTab from '../linkedTab';
import ProjectActions from './projectActions';
import ProjectOverview from './projectOverview';

export interface Props {
  project: ProjectModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.ProjectAction;
  onDelete: () => actions.ProjectAction;
  onArchive: () => actions.ProjectAction;
  onRestore: () => actions.ProjectAction;
  fetchData: () => actions.ProjectAction;
  bookmark: () => actions.ProjectAction;
  unbookmark: () => actions.ProjectAction;
  startNotebook: () => actions.ProjectAction;
  stopNotebook: () => actions.ProjectAction;
  startTensorboard: () => actions.ProjectAction;
  stopTensorboard: () => actions.ProjectAction;
}

export default class ProjectDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const project = this.props.project;
    if (_.isNil(project)) {
      return EmptyList(false, 'project', 'project');
    }

    const bookmark: BookmarkInterface = getBookmark(
      this.props.project.bookmarked, this.props.bookmark, this.props.unbookmark);
    const projectUrl = getProjectUrl(project.user, project.name);

    return (
      <div className="row">
        <div className="col-md-12">
          <Breadcrumb
            icon="fa-server"
            links={[
              {name: project.user, value: getUserUrl(project.user)},
              {name: project.name}]}
            bookmark={bookmark}
            actions={
              <ProjectActions
                onDelete={this.props.onDelete}
                onArchive={project.deleted ? undefined : this.props.onArchive}
                onRestore={project.deleted ? this.props.onRestore : undefined}
                notebookActionCallback={
                  project.has_notebook ? this.props.stopNotebook : this.props.startNotebook}
                tensorboardActionCallback={
                  project.has_tensorboard ? this.props.stopTensorboard : this.props.startTensorboard}
                hasNotebook={project.has_notebook}
                hasTensorboard={project.has_tensorboard}
                pullRight={true}
              />
            }
          />
          <LinkedTab
            baseUrl={projectUrl}
            tabs={[
              {
                title: 'Overview',
                component: <ProjectOverview
                  project={project}
                  onUpdate={this.props.onUpdate}
                />,
                relUrl: ''
              }, {
                title: 'Experiments',
                component: <Experiments
                  user={project.user}
                  projectName={project.unique_name}
                  showBookmarks={true}
                  useCheckbox={true}
                  useFilters={true}
                />,
                relUrl: 'experiments'
              }, {
                title: 'Experiment groups',
                component: <Groups
                  user={project.user}
                  projectName={project.unique_name}
                  showBookmarks={true}
                  useFilters={true}
                />,
                relUrl: 'groups'
              }, {
                title: 'Jobs',
                component: <Jobs
                  user={project.user}
                  projectName={project.unique_name}
                  showBookmarks={true}
                  useFilters={true}
                />,
                relUrl: 'jobs'
              }, {
                title: 'Builds',
                component: <Builds
                  user={project.user}
                  projectName={project.unique_name}
                  showBookmarks={true}
                  useFilters={true}
                />,
                relUrl: 'builds'
              }, {
                title: 'Activity logs',
                component: <ActivityLogs user={project.user} projectName={project.name}/>,
                relUrl: 'activitylogs'
              }, {
                title: 'Instructions',
                component: <ProjectInstructions projectName={project.unique_name}/>,
                relUrl: 'instructions'
              }
            ]}
          />
        </div>
      </div>
    );
  }
}
