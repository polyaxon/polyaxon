import * as React from 'react';
import { Link } from 'react-router-dom';

import {
  ClusterAuthAzureSettingsURL,
  ClusterAuthBitbucketSettingsURL,
  ClusterAuthGithubSettingsURL,
  ClusterAuthGitlabSettingsURL
} from '../../../urls/routes/settings/auth';
import {
  ClusterIntegrationsSettingsURL,
  ClusterMoreSettingsURL,
  ClusterReposSettingsURL } from '../../../urls/routes/settings/base';
import {
  ClusterHardwareSettingsURL,
  ClusterSchedulingBuildJobsSettingsURL,
  ClusterSchedulingExperimentsSettingsURL,
  ClusterSchedulingJobsSettingsURL,
  ClusterSchedulingNotebooksSettingsURL,
  ClusterSchedulingTensorboardsSettingsURL,
} from '../../../urls/routes/settings/scheduling';

import '../sidebar.less';

export default class SettingsSidebar extends React.Component<{}, {}> {

  public render() {
    const currentPath = location.pathname;

    return (
      <div className="row">
        <nav className="nav menu nav-stacked">
          <h3 className="menu-heading">Scheduling</h3>
          <Link
            className={currentPath === ClusterSchedulingBuildJobsSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterSchedulingBuildJobsSettingsURL}
          >Builds scheduling
          </Link>
          <Link
            className={currentPath === ClusterSchedulingJobsSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterSchedulingJobsSettingsURL}
          >
            Jobs scheduling
          </Link>
          <Link
            className={currentPath === ClusterSchedulingExperimentsSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterSchedulingExperimentsSettingsURL}
          >
            Experiments scheduling
          </Link>
          <Link
            className={currentPath === ClusterSchedulingNotebooksSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterSchedulingNotebooksSettingsURL}
          >
            Notebooks scheduling
          </Link>
          <Link
            className={currentPath === ClusterSchedulingTensorboardsSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterSchedulingTensorboardsSettingsURL}
          >
            Tensorboards scheduling
          </Link>
        </nav>
        <nav className="nav menu nav-stacked">
          <h3 className="menu-heading">Auth</h3>
          <Link
            className={currentPath === ClusterAuthGithubSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterAuthGithubSettingsURL}
          >
            Github
          </Link>
          <Link
            className={currentPath === ClusterAuthGitlabSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterAuthGitlabSettingsURL}
          >
            Gitlab
          </Link>
          <Link
            className={currentPath === ClusterAuthBitbucketSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterAuthBitbucketSettingsURL}
          >
            Bitbucket
          </Link>
          <Link
            className={currentPath === ClusterAuthAzureSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterAuthAzureSettingsURL}
          >
            Azure
          </Link>
        </nav>
        <nav className="nav menu nav-stacked">
          <h3 className="menu-heading">Other options</h3>
          <Link
            className={currentPath === ClusterReposSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterReposSettingsURL}
          >
            Private repos
          </Link>
          <Link
            className={currentPath === ClusterIntegrationsSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterIntegrationsSettingsURL}
          >
            Integrations
          </Link>
          <Link
            className={currentPath === ClusterHardwareSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterHardwareSettingsURL}
          >
            Hardware accelerator settings
          </Link>
          <Link
            className={currentPath === ClusterMoreSettingsURL ? 'active menu-item' : 'menu-item'}
            to={ClusterMoreSettingsURL}
          >
            More options
          </Link>
        </nav>
      </div>
    );
  }
}
