import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/group';
import { isDone } from '../../constants/statuses';
import { getGroupUrl, getProjectUrl, getUserUrl, splitUniqueName } from '../../constants/utils';
import Experiments from '../../containers/experiments';
import Metrics from '../../containers/metrics';
import Statuses from '../../containers/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { GroupModel } from '../../models/group';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import { EmptyList } from '../empty/emptyList';
import GroupInstructions from '../instructions/groupInstructions';
import LinkedTab from '../linkedTab';
import YamlText from '../yamlText';
import GroupActions from './groupActions';
import GroupOverview from './groupOverview';

export interface Props {
  group: GroupModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.GroupAction;
  onDelete: () => actions.GroupAction;
  onStop: () => actions.GroupAction;
  onArchive: () => actions.GroupAction;
  onRestore: () => actions.GroupAction;
  fetchData: () => actions.GroupAction;
  bookmark: () => actions.GroupAction;
  unbookmark: () => actions.GroupAction;
  startTensorboard: () => actions.GroupAction;
  stopTensorboard: () => actions.GroupAction;
}

export default class GroupDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const group = this.props.group;
    if (_.isNil(group)) {
      return EmptyList(false, 'experiment group', 'group');
    }

    const bookmark: BookmarkInterface = getBookmark(
      this.props.group.bookmarked, this.props.bookmark, this.props.unbookmark);
    const values = splitUniqueName(group.project);
    const groupUrl = getGroupUrl(values[0], values[1], this.props.group.id);
    const projectUrl = getProjectUrl(values[0], values[1]);
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fa-cubes"
              links={[
                {name: values[0], value: getUserUrl(values[0])},
                {name: values[1], value: projectUrl},
                {name: 'Groups', value: `${projectUrl}#groups`},
                {name: `Group ${group.id}`}]}
              bookmark={bookmark}
              actions={
                <GroupActions
                  onDelete={this.props.onDelete}
                  onStop={group.group_type === 'study' ? this.props.onStop : undefined}
                  onArchive={group.deleted ? undefined : this.props.onArchive}
                  onRestore={group.deleted ? this.props.onRestore : undefined}
                  tensorboardActionCallback={
                  group.has_tensorboard ? this.props.stopTensorboard : this.props.startTensorboard}
                  hasTensorboard={group.has_tensorboard}
                  isRunning={!isDone(group.last_status)}
                  pullRight={true}
                />
              }
            />
            <LinkedTab
              baseUrl={groupUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <GroupOverview
                    group={group}
                    onUpdate={this.props.onUpdate}
                    onFetch={this.props.fetchData}
                  />,
                  relUrl: ''
                }, {
                  title: 'Experiments',
                  component: <Experiments
                    user={group.user}
                    projectName={group.project}
                    groupId={group.id}
                    isSelection={group.group_type === 'selection'}
                    showBookmarks={true}
                    useCheckbox={true}
                    useFilters={true}
                  />,
                  relUrl: 'experiments'
                },
                {
                  title: 'Metrics',
                  component: <Metrics
                    project={group.project}
                    resource="groups"
                    id={group.id}
                    chartTypes={['line', 'bar', 'scatter', 'histogram']}
                  />,
                  relUrl: 'metrics'
                },
                {
                  title: 'Statuses',
                  component: <Statuses
                    project={group.project}
                    resource="groups"
                    id={group.id}
                  />,
                  relUrl: 'statuses'
                }, {
                  title: 'Config',
                  component: <YamlText title="Config" configText={group.content}/>,
                  relUrl: 'config'
                }, {
                  title: 'Instructions',
                  component: <GroupInstructions id={group.id}/>,
                  relUrl: 'instructions'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}
