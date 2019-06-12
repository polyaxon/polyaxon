import * as React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import ClusterActivityLogs from '../components/activitylogs/clusterActivityLogs';
import HistoryLogs from '../components/activitylogs/histroyLogs';
import Archives from '../containers/archives';
import Bookmarks from '../containers/bookmarks';
import HealthStatus from '../containers/healthStatus';
import ProjectDetail from '../containers/projects/projectDetail';
import Token from '../containers/token';
import User from '../containers/user';
import {
  archivesURL,
  bookmarksURL,
  clusterActivityLogsURL,
  historyLogsURL,
  newEntityURL,
  projectURL,
  settingsURL,
  statusURL,
  tokenURL,
  userURL,
} from '../urls/routes/base';
import { getHomeUrl } from '../urls/utils';
import NewEntityRoutes from './new';
import ProjectRoutes from './projects';
import SettingsRoutes from './settings/base';

const Routes = () => {
  return (
    <Switch>
      <Route path={tokenURL} exact={true} component={Token}/>
      <Route path={statusURL} exact={true} component={HealthStatus}/>
      <Route path={historyLogsURL} exact={true} component={HistoryLogs}/>
      <Route path={clusterActivityLogsURL} exact={true} component={ClusterActivityLogs}/>
      <Route path={bookmarksURL} exact={true} component={Bookmarks}/>
      <Route path={archivesURL} exact={true} component={Archives}/>
      <Route path={newEntityURL} component={NewEntityRoutes}/>
      <Route path={settingsURL} component={SettingsRoutes}/>
      <Route path={projectURL} exact={true} component={ProjectDetail}/>
      <Route path={projectURL} component={ProjectRoutes}/>
      <Route path={userURL} component={User}/>

      <Route path="*" render={() => <Redirect to={getHomeUrl()}/>}/>
    </Switch>
  );
};

export default Routes;
