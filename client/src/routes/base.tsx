import * as React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import ClusterActivityLogs from '../components/activitylogs/clusterActivityLogs';
import HistoryLogs from '../components/activitylogs/histroyLogs';
import { getHomeUrl } from '../constants/utils';
import Archives from '../containers/archives';
import Bookmarks from '../containers/bookmarks';
import HealthStatus from '../containers/healthStatus';
import ProjectDetail from '../containers/projects/projectDetail';
import Token from '../containers/token';
import User from '../containers/user';
import NewEntityRoutes from './new';
import ProjectRoutes from './projects';

const Routes = () => {
  const tokenRoute = '/app/token/';
  const statusRoute = '/app/status/';
  const clusterActivityLogsRoute = '/app/activitylogs/';
  const historyLogsRoute = '/app/historylogs/';
  const newEntity = '/app/new/';
  const bookmarksRoute = '/app/bookmarks/:user/';
  const archivesRoute = '/app/archives/:user/';
  const userRoute = '/app/:user/';
  const projectDetailRoute = '/app/:user/:projectName/';

  return (
    <Switch>
      <Route path={tokenRoute} exact={true} component={Token}/>
      <Route path={statusRoute} exact={true} component={HealthStatus}/>
      <Route path={historyLogsRoute} exact={true} component={HistoryLogs}/>
      <Route path={clusterActivityLogsRoute} exact={true} component={ClusterActivityLogs}/>
      <Route path={bookmarksRoute} exact={true} component={Bookmarks}/>
      <Route path={archivesRoute} exact={true} component={Archives}/>
      <Route path={newEntity} component={NewEntityRoutes}/>
      <Route path={projectDetailRoute} exact={true} component={ProjectDetail}/>
      <Route path={projectDetailRoute} component={ProjectRoutes}/>
      <Route path={userRoute} component={User}/>

      <Route path="*" render={() => <Redirect to={getHomeUrl()}/>}/>
    </Switch>
  );
};

export default Routes;
