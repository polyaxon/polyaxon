import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import GeneralSettings from '../../containers/settings/general';
import KeyOption from '../../containers/settings/keyOption';
import { ClusterMopreSettingsURL } from '../../options/general';
import { ClusterHardwareSettingsURL, HARDWARE_KEYS } from '../../options/hardware';
import { ClusterIntegrationsSettingsURL, INTEGRATIONS_KEYS } from '../../options/integrations';
import { ClusterReposSettingsURL, REPOS_KEYS } from '../../options/repos';
import AuthSettingsRoutes from './auth';
import SchedulingSettingsRoutes from './scheduling';

const SettingsRoutes = () => {
  const ClusterSchedulingSettingsURL = '/app/settings/scheduling/';
  const ClusterAuthSettingsURL = '/app/settings/auth/';

  return (
    <Switch>
      <Route path={ClusterSchedulingSettingsURL} component={SchedulingSettingsRoutes}/>
      <Route path={ClusterAuthSettingsURL} component={AuthSettingsRoutes}/>
      <Route
        path={ClusterReposSettingsURL}
        component={() => <GeneralSettings
          section="Private repos"
          options={REPOS_KEYS}
        />}
      />
      <Route
        path={ClusterIntegrationsSettingsURL}
        component={() => <GeneralSettings
          section="Integrations"
          options={INTEGRATIONS_KEYS}
        />}
      />
      <Route
        path={ClusterHardwareSettingsURL}
        component={() => <GeneralSettings
          section="Hardware Accelerators"
          options={HARDWARE_KEYS}
        />}
      />
      <Route
        path={ClusterMopreSettingsURL}
        component={KeyOption}
      />
    </Switch>
  );
};

export default SettingsRoutes;
