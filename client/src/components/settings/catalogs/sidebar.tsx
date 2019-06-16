import * as React from 'react';
import { Link } from 'react-router-dom';

import {
  ClusterDatasetsCatalogURL,
  ClusterK8SConfigMapsCatalogURL,
  ClusterK8SSecretsCatalogURL,
  ClusterRegistriesCatalogURL,
  ClusterReposCatalogURL,
} from '../../../urls/routes/catalogs';

import '../sidebar.less';

export default class CatalogsSidebar extends React.Component<{}, {}> {

  public render() {
    const currentPath = location.pathname;

    return (
      <div className="row">
        <nav className="nav menu nav-stacked">
          <h3 className="menu-heading">Catalogs</h3>
          <Link
            className={currentPath === ClusterDatasetsCatalogURL ? 'active menu-item' : 'menu-item'}
            to={ClusterDatasetsCatalogURL}
          >
            Data
          </Link>
          <Link
            className={currentPath === ClusterK8SConfigMapsCatalogURL ? 'active menu-item' : 'menu-item'}
            to={ClusterK8SConfigMapsCatalogURL}
          >
            Config Maps
          </Link>
          <Link
            className={currentPath === ClusterK8SSecretsCatalogURL ? 'active menu-item' : 'menu-item'}
            to={ClusterK8SSecretsCatalogURL}
          >
            Secrets
          </Link>
          <Link
            className={currentPath === ClusterRegistriesCatalogURL ? 'active menu-item' : 'menu-item'}
            to={ClusterRegistriesCatalogURL}
          >
            Registries
          </Link>
          <Link
            className={currentPath === ClusterReposCatalogURL ? 'active menu-item' : 'menu-item'}
            to={ClusterReposCatalogURL}
          >
            Git
          </Link>
        </nav>
      </div>
    );
  }
}
