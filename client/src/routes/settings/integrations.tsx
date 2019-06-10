import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import GeneralSettings from '../../containers/settings/general';
import { INTEGRATIONS_KEYS } from '../../options/integrations';

const AuthSettingsRoutes = () => {
  const ClusterAuthGithubSettings = '/app/settings/auth/github/';

  return (
    <Switch>
      <Route
        path={ClusterAuthGithubSettings}
        component={() => <GeneralSettings
          section="Integrations"
          options={INTEGRATIONS_KEYS}
        />}
      />
    </Switch>
  );
};

export default AuthSettingsRoutes;
