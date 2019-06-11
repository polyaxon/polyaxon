import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import GeneralSettings from '../../containers/settings/configs/general';
import { BUILD_JOB_KEYS, ClusterSchedulingBuildJobsSettingsURL } from '../../options/build_jobs';
import { ClusterSchedulingExperimentsSettingsURL, EXPERIMENT_KEYS } from '../../options/experiments';
import { ClusterSchedulingJobsSettingsURL, JOB_KEYS } from '../../options/jobs';
import { ClusterSchedulingNotebooksSettingsURL, NOTEBOOK_KEYS } from '../../options/notebooks';
import { ClusterSchedulingTensorboardsSettingsURL, TENSORBOARD_KEYS } from '../../options/tensorboards';

const SchedulingSettingsRoutes = () => {

  return (
    <Switch>
      <Route
        path={ClusterSchedulingBuildJobsSettingsURL}
        component={() => <GeneralSettings
          section="Build Jobs Scheduling"
          options={BUILD_JOB_KEYS}
        />}
      />
      <Route
        path={ClusterSchedulingJobsSettingsURL}
        component={() => <GeneralSettings
          section="Jobs Scheduling"
          options={JOB_KEYS}
        />}
      />
      <Route
        path={ClusterSchedulingExperimentsSettingsURL}
        component={() => <GeneralSettings
          section="Experiments Scheduling"
          options={EXPERIMENT_KEYS}
        />}
      />
      <Route
        path={ClusterSchedulingNotebooksSettingsURL}
        component={() => <GeneralSettings
          section="Notebooks Scheduling"
          options={NOTEBOOK_KEYS}
        />}
      />
      <Route
        path={ClusterSchedulingTensorboardsSettingsURL}
        component={() => <GeneralSettings
          section="Tensorboards Scheduling"
          options={TENSORBOARD_KEYS}
        />}
      />
    </Switch>
  );
};

export default SchedulingSettingsRoutes;
