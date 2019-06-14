import * as React from 'react';
import { Route, Switch } from 'react-router-dom';

import K8SResources from '../../containers/settings/catalogs/k8sResources';
import Stores from '../../containers/settings/catalogs/stores';
import {
  ClusterDatasetsCatalogURL,
  ClusterK8SConfigMapsCatalogURL,
  ClusterK8SSecretsCatalogURL
} from '../../urls/routes/catalogs';

const CatalogsRoutes = () => {

  return (
    <Switch>
      <Route
        path={ClusterK8SConfigMapsCatalogURL}
        component={() => <K8SResources resource="k8s_config_maps" showDeleted={false}/>}
      />
      <Route
        path={ClusterK8SSecretsCatalogURL}
        component={() => <K8SResources resource="k8s_secrets" showDeleted={false}/>}
      />
      <Route
        path={ClusterDatasetsCatalogURL}
        component={() => <Stores resource="data_stores" showDeleted={false}/>}
      />
    </Switch>
  );
};

export default CatalogsRoutes;
