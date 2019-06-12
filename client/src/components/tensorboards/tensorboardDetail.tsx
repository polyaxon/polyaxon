import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/tensorboards';
import { isDone } from '../../constants/statuses';
import Statuses from '../../containers/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { TensorboardModel } from '../../models/tensorboard';
import { getProjectUrl, getTensorboardApiUrl, getUserUrl, splitUniqueName, } from '../../urls/utils';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import YamlText from '../editors/yamlText';
import { EmptyList } from '../empty/emptyList';
import TensorboardInstructions from '../instructions/tensorboardInstructions';
import LinkedTab from '../linkedTab';
import TensorboardActions from './tensorboardActions';
import TensorboardOverview from './tensorboardOverview';

export interface Props {
  tensorboard: TensorboardModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.TensorboardAction;
  onDelete: () => actions.TensorboardAction;
  onArchive: () => actions.TensorboardAction;
  onRestore: () => actions.TensorboardAction;
  onStop: () => actions.TensorboardAction;
  fetchData: () => actions.TensorboardAction;
  bookmark: () => actions.TensorboardAction;
  unbookmark: () => actions.TensorboardAction;
}

export default class TensorboardDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const tensorboard = this.props.tensorboard;
    if (_.isNil(tensorboard)) {
      return EmptyList(false, 'tensorboard', 'tensorboard');
    }

    const bookmark: BookmarkInterface = getBookmark(
      this.props.tensorboard.bookmarked, this.props.bookmark, this.props.unbookmark);
    const values = splitUniqueName(tensorboard.project);
    const tensorboardUrl = getTensorboardApiUrl(values[0], values[1], this.props.tensorboard.id);
    const projectUrl = getProjectUrl(values[0], values[1]);
    const breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: projectUrl},
      {name: 'Tensorboards', value: `${projectUrl}#tensorboards`},
      {name: `Tensorboard ${tensorboard.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fas fa-gavel"
              links={breadcrumbLinks}
              bookmark={bookmark}
              actions={
                <TensorboardActions
                  onDelete={this.props.onDelete}
                  onStop={this.props.onStop}
                  onArchive={tensorboard.deleted ? undefined : this.props.onArchive}
                  onRestore={tensorboard.deleted ? this.props.onRestore : undefined}
                  isRunning={!isDone(this.props.tensorboard.last_status)}
                  pullRight={true}
                />
              }
            />
            <LinkedTab
              baseUrl={tensorboardUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <TensorboardOverview
                    tensorboard={tensorboard}
                    onUpdate={this.props.onUpdate}
                    onFetch={this.props.fetchData}
                  />,
                  relUrl: ''
                }, {
                  title: 'Statuses',
                  component: <Statuses
                    project={tensorboard.project}
                    resource="tensorboards"
                    id={tensorboard.id}
                  />,
                  relUrl: 'statuses'
                }, {
                  title: 'Config',
                  component: <YamlText title="Config" configText={tensorboard.content}/>,
                  relUrl: 'config'
                }, {
                  title: 'Instructions',
                  component: <TensorboardInstructions id={tensorboard.id}/>,
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
