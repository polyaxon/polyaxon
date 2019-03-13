import * as jsYaml from 'js-yaml';
import * as _ from 'lodash';
import * as React from 'react';

import CopyToClipboard from './copyToClipboard';

import './text.less';

export interface Props {
  title: string;
  config?: { [key: string]: any };
  configText?: string;
}

function YamlText({config, configText, title}: Props) {
  if (!_.isNil(configText)) {
    config = jsYaml.safeLoad(configText);
  }

  const orderedConfig: { [key: string]: any } = {};
  if (!_.isNil(config)) {
    if (!_.isNil(config.version)) {
      orderedConfig.version = config.version;
    }
    if (!_.isNil(config.kind)) {
      orderedConfig.kind = config.kind;
    }
    if (!_.isNil(config.logging)) {
      orderedConfig.logging = config.logging;
    }
    if (!_.isNil(config.backend)) {
      orderedConfig.backend = config.backend;
    }
    if (!_.isNil(config.framework)) {
      orderedConfig.framework = config.framework;
    }
    if (!_.isNil(config.hptuning)) {
      orderedConfig.hptuning = config.hptuning;
    }
    if (!_.isNil(config.environment)) {
      orderedConfig.environment = config.environment;
    }
    if (!_.isNil(config.declarations)) {
      orderedConfig.declarations = config.declarations;
    }
    if (!_.isNil(config.build)) {
      orderedConfig.build = config.build;
    }
    if (!_.isNil(config.image)) {
      orderedConfig.image = config.image;
    }
    if (!_.isNil(config.dockerfile)) {
      orderedConfig.dockerfile = config.dockerfile;
    }
    if (!_.isNil(config.context)) {
      orderedConfig.context = config.context;
    }
    if (!_.isNil(config.build_steps)) {
      orderedConfig.build_steps = config.build_steps;
    }
    if (!_.isNil(config.env_vars)) {
      orderedConfig.env_vars = config.env_vars;
    }
    if (!_.isNil(config.branch)) {
      orderedConfig.branch = config.branch;
    }
    if (!_.isNil(config.commit)) {
      orderedConfig.commit = config.commit;
    }
    if (!_.isNil(config.nocache)) {
      orderedConfig.nocache = config.nocache;
    }
    if (!_.isNil(config.run)) {
      orderedConfig.run = config.run;
    }
  }

  // const copyToClipboard = (e: any) => {
  //   const copyArea = document.getElementById('yaml-content');
  //   if (copyArea) {
  //     copyArea.select();
  //     document.execCommand('copy');
  //     // This is just personal preference.
  //     // I prefer to not show the the whole text area selected.
  //     e.target.focus();
  //   }
  // };

  // const textAreaRef = useRef(null);

  const processedText = (!_.isNil(config)) ?
    jsYaml.dump(orderedConfig) :
    'No content!';

  function getText() {
    return (
      <div className="text yaml">
        <div className="row">
          <div className="col-md-12">
            <div className="text-header">
              {title}
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="text-content">
              <CopyToClipboard text={processedText}>
                <span className="pull-right btn btn-sm btn-default">
                  <i className={`fas fa-copy icon`} aria-hidden="true"/> Copy
                </span>
              </CopyToClipboard>
              <p>{processedText}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (getText());
}

export default YamlText;
