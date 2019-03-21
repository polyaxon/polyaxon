import * as React from 'react';
import AceEditor from 'react-ace';

import 'brace/mode/dockerfile';
import 'brace/theme/github';

import CopyToClipboard from './copyToClipboard';

import './text.less';

export interface Props {
  title: string;
  text: string;
}

function DockerfileText({title, text}: Props) {

  function getText() {
    if (!(text && text.length > 0)) {
      return (<p>No content!</p>);
    }

    return (
      <div className="text code-text">
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
              <CopyToClipboard text={text}>
                <span className="pull-right btn btn-sm btn-default text-copy">
                  <i className={`fas fa-copy icon`} aria-hidden="true"/> Copy
                </span>
              </CopyToClipboard>
              <AceEditor
                mode="dockerfile"
                theme="github"
                name="UNIQUE_ID_OF_DIV"
                value={text}
                readOnly={true}
                width="auto"
                editorProps={{$blockScrolling: true}}
              />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (getText());
}

export default DockerfileText;
