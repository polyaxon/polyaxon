import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import GeneralSettings from '../../containers/settings/configs/general';
import KeyOption from '../../containers/settings/configs/keyOption';
import { HARDWARE_KEYS } from '../../options/hardware';
import { INTEGRATIONS_KEYS } from '../../options/integrations';
import { REPOS_KEYS } from '../../options/repos';
import { authSettingsURL, schedulingSettingsURL } from '../../urls/routes/base';
import {
  ClusterIntegrationsSettingsURL,
  ClusterMoreSettingsURL,
  ClusterReposSettingsURL
} from '../../urls/routes/settings/base';
import { ClusterHardwareSettingsURL } from '../../urls/routes/settings/scheduling';
import AuthSettingsRoutes from './auth';
import SchedulingSettingsRoutes from './scheduling';

const SettingsRoutes = () => {
  return (
    <Switch>
      <Route path={schedulingSettingsURL} component={SchedulingSettingsRoutes}/>
      <Route path={authSettingsURL} component={AuthSettingsRoutes}/>
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
        path={ClusterMoreSettingsURL}
        component={KeyOption}
      />
    </Switch>
  );
};

export default SettingsRoutes;
