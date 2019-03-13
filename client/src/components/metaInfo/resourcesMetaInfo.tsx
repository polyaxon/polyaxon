import * as React from 'react';

export interface Props {
  resources?: {[key: string]: any};
}

function ResourcesMetaInfo({resources}: Props) {
  const component = resources ? (
    <div className="meta meta-resources">
      {Object.keys(resources)
        .filter(
          (res, idx) =>
            resources[res] != null
        )
        .map(
          (res, idx) =>
            <span className="meta-info" key={idx}>
                <i className="fas fa-microchip icon" aria-hidden="true"/>
                <span className="title">{res}:</span>
              {resources[res].requests || ''} - {resources[res].limits || ''}
              </span>
        )}
    </div>
  ) : null;
  return component;
}

export default ResourcesMetaInfo;
