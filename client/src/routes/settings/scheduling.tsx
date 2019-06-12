import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import GeneralSettings from '../../containers/settings/configs/general';
import { BUILD_JOB_KEYS } from '../../options/build_jobs';
import { EXPERIMENT_KEYS } from '../../options/experiments';
import { JOB_KEYS } from '../../options/jobs';
import { NOTEBOOK_KEYS } from '../../options/notebooks';
import { TENSORBOARD_KEYS } from '../../options/tensorboards';
import {
  ClusterSchedulingBuildJobsSettingsURL,
  ClusterSchedulingExperimentsSettingsURL,
  ClusterSchedulingJobsSettingsURL,
  ClusterSchedulingNotebooksSettingsURL,
  ClusterSchedulingTensorboardsSettingsURL,
} from '../../urls/routes/settings/scheduling';

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
