import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/build';
import { isDone } from '../../constants/statuses';
import { getBuildUrl, getProjectUrl, getUserUrl, splitUniqueName, } from '../../constants/utils';
import Logs from '../../containers/logs';
import Statuses from '../../containers/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { BuildModel } from '../../models/build';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import { EmptyList } from '../empty/emptyList';
import BuildInstructions from '../instructions/buildInstructions';
import LinkedTab from '../linkedTab';
import Text from '../text';
import YamlText from '../yamlText';
import BuildActions from './buildActions';
import BuildOverview from './buildOverview';

export interface Props {
  build: BuildModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.BuildAction;
  onDelete: () => actions.BuildAction;
  onArchive: () => actions.BuildAction;
  onRestore: () => actions.BuildAction;
  onStop: () => actions.BuildAction;
  fetchData: () => actions.BuildAction;
  bookmark: () => actions.BuildAction;
  unbookmark: () => actions.BuildAction;
}

export default class BuildDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const build = this.props.build;
    if (_.isNil(build)) {
      return EmptyList(false, 'build', 'build');
    }

    const bookmark: BookmarkInterface = getBookmark(
      this.props.build.bookmarked, this.props.bookmark, this.props.unbookmark);
    const values = splitUniqueName(build.project);
    const buildUrl = getBuildUrl(values[0], values[1], this.props.build.id);
    const projectUrl = getProjectUrl(values[0], values[1]);
    const breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: projectUrl},
      {name: 'Builds', value: `${projectUrl}#builds`},
      {name: `Build ${build.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fa-gavel"
              links={breadcrumbLinks}
              bookmark={bookmark}
              actions={
                <BuildActions
                  onDelete={this.props.onDelete}
                  onStop={this.props.onStop}
                  onArchive={build.deleted ? undefined : this.props.onArchive}
                  onRestore={build.deleted ? this.props.onRestore : undefined}
                  isRunning={!isDone(this.props.build.last_status)}
                  pullRight={true}
                />
              }
            />
            <LinkedTab
              baseUrl={buildUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <BuildOverview
                    build={build}
                    onUpdate={this.props.onUpdate}
                    onFetch={this.props.fetchData}
                  />,
                  relUrl: ''
                }, {
                  title: 'Logs',
                  component: <Logs
                    fetchData={() => null}
                    logs={''}
                    project={build.project}
                    resource="builds"
                    id={build.id}
                  />,
                  relUrl: 'logs'
                }, {
                  title: 'Dockerfile',
                  component: <Text title="Dockerfile" text={build.dockerfile}/>,
                  relUrl: 'dockerfile'
                }, {
                  title: 'Statuses',
                  component: <Statuses
                    project={build.project}
                    resource="builds"
                    id={build.id}
                  />,
                  relUrl: 'statuses'
                }, {
                  title: 'Config',
                  component: <YamlText title="Config" config={build.config}/>,
                  relUrl: 'config'
                }, {
                  title: 'Instructions',
                  component: <BuildInstructions id={build.id}/>,
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
