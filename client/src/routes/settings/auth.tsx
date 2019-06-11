import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import GeneralSettings from '../../containers/settings/configs/general';
import {
  AUTH_AZURE_KEYS,
  AUTH_BITBUCKET_KEYS,
  AUTH_GITHUB_KEYS,
  AUTH_GITLAB_KEYS,
  ClusterAuthAzureSettingsURL,
  ClusterAuthBitbucketSettingsURL,
  ClusterAuthGithubSettingsURL,
  ClusterAuthGitlabSettingsURL
} from '../../options/auth';

const AuthSettingsRoutes = () => {
  return (
    <Switch>
      <Route
        path={ClusterAuthGithubSettingsURL}
        component={() => <GeneralSettings
          section="Auth Github"
          options={AUTH_GITHUB_KEYS}
        />}
      />
      <Route
        path={ClusterAuthGitlabSettingsURL}
        component={() => <GeneralSettings
          section="Auth GitLab"
          options={AUTH_GITLAB_KEYS}
        />}
      />
      <Route
        path={ClusterAuthBitbucketSettingsURL}
        component={() => <GeneralSettings
          section="Auth Bitbucket"
          options={AUTH_BITBUCKET_KEYS}
        />}
      />
      <Route
        path={ClusterAuthAzureSettingsURL}
        component={() => <GeneralSettings
          section="Auth Azure"
          options={AUTH_AZURE_KEYS}
        />}
      />
    </Switch>
  );
};

export default AuthSettingsRoutes;
